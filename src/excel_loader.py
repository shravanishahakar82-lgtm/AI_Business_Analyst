import re
import pandas as pd


# ============================================================
# EXCEL LOADER
# Keeps the ORIGINAL dashboard unchanged.
# Converts different Excel layouts into the standard structure
# expected by dashboard.py.
# ============================================================


def _normalize_column_name(name):
    """Make Excel column names easy to compare."""
    name = str(name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def _find_column(columns, candidates):
    """Find a matching column from common Excel column names."""

    columns = list(columns)

    # 1. Exact match
    for candidate in candidates:
        if candidate in columns:
            return candidate

    # 2. Safe substring match
    for column in columns:
        for candidate in candidates:
            if (
                candidate in column
                or column in candidate
            ):
                return column

    return None


def _find_sales_sheet(uploaded_file):
    """
    Search every worksheet and find the sheet that contains
    business/sales headers.

    This prevents problems when the workbook has:
    - Instructions
    - Dashboard
    - Data Dictionary
    - Raw Data
    - Analysis sheets
    """

    sheets = pd.read_excel(
        uploaded_file,
        sheet_name=None,
        header=None
    )

    required_signals = {
        "order_id": [
            "order_id",
            "order",
            "order_number",
            "order_no",
            "transaction_id",
            "transactionid",
            "invoice_id",
            "invoice_no",
        ],
        "date": [
            "order_date",
            "orderdate",
            "sales_date",
            "transaction_date",
            "invoice_date",
            "date",
        ],
        "product": [
            "product_name",
            "productname",
            "product",
            "item_name",
            "item",
        ],
        "revenue": [
            "revenue",
            "sales",
            "sales_amount",
            "sales_value",
            "amount",
            "total_sales",
            "total_amount",
            "turnover",
        ],
    }

    best_sheet = None
    best_header_row = None
    best_score = -1

    for sheet_name, raw in sheets.items():

        if raw.empty:
            continue

        # Search the first 15 rows for the actual header row.
        max_rows = min(15, len(raw))

        for row_number in range(max_rows):

            values = [
                _normalize_column_name(value)
                for value in raw.iloc[row_number].tolist()
                if pd.notna(value)
            ]

            if not values:
                continue

            score = 0

            for candidates in required_signals.values():

                if any(
                    value in candidates
                    for value in values
                ):
                    score += 1

            # Product + date + order/revenue is a strong
            # indication that this is the sales sheet.
            if score > best_score:

                best_score = score
                best_sheet = sheet_name
                best_header_row = row_number

    if best_sheet is None or best_score < 2:

        raise ValueError(
            "Could not find a sales-data sheet in the Excel workbook. "
            "Make sure one sheet contains columns such as "
            "Order ID, Order Date, Product, Quantity, Price/Revenue, "
            "Customer and Region."
        )

    return sheets, best_sheet, best_header_row


def load_excel_file(uploaded_file):
    """
    Read the uploaded Excel workbook.

    The function searches all worksheets and automatically finds
    the actual sales-data header row.
    """

    sheets, sheet_name, header_row = _find_sales_sheet(
        uploaded_file
    )

    raw = sheets[sheet_name]

    # Read the selected sheet again using the detected header.
    df = pd.read_excel(
        uploaded_file,
        sheet_name=sheet_name,
        header=header_row
    )

    # Remove completely empty rows/columns.
    df = (
        df
        .dropna(how="all")
        .dropna(axis=1, how="all")
        .copy()
    )

    # Normalize headers.
    df.columns = [
        _normalize_column_name(column)
        for column in df.columns
    ]

    # Remove accidental "Unnamed" columns.
    df = df[
        [
            column
            for column in df.columns
            if not str(column).startswith("unnamed")
        ]
    ]

    # Store source information without changing the DataFrame.
    df.attrs["source_sheet"] = sheet_name
    df.attrs["header_row"] = header_row + 1

    return df


def validate_business_data(df):
    """
    Basic validation before preparing the data.
    """

    if df is None or df.empty:

        return (
            False,
            "The uploaded Excel file is empty."
        )

    if len(df.columns) < 2:

        return (
            False,
            "The Excel file must contain at least 2 columns."
        )

    return (
        True,
        "Excel file loaded successfully."
    )


def prepare_excel_data(df):
    """
    Convert Excel data into the SAME two-table structure
    used by the original database dashboard.

    Returns:
        ((orders, order_items), [])
    or
        (None, missing_columns)
    """

    df = df.copy()

    # ========================================================
    # 1. COLUMN DETECTION
    # ========================================================

    order_id_col = _find_column(
        df.columns,
        [
            "order_id",
            "orderid",
            "order_number",
            "order_no",
            "transaction_id",
            "transactionid",
            "invoice_id",
            "invoice_no",
            "id",
        ]
    )

    date_col = _find_column(
        df.columns,
        [
            "order_date",
            "orderdate",
            "sales_date",
            "transaction_date",
            "invoice_date",
            "date",
        ]
    )

    product_col = _find_column(
        df.columns,
        [
            "product_name",
            "productname",
            "product",
            "item_name",
            "item",
        ]
    )

    category_col = _find_column(
        df.columns,
        [
            "category",
            "product_category",
            "productcategory",
            "type",
            "segment",
        ]
    )

    customer_col = _find_column(
        df.columns,
        [
            "customer_name",
            "customername",
            "customer",
            "client",
            "buyer",
        ]
    )

    region_col = _find_column(
        df.columns,
        [
            "region",
            "location",
            "area",
            "zone",
            "territory",
        ]
    )

    quantity_col = _find_column(
        df.columns,
        [
            "quantity",
            "qty",
            "units",
            "unit_sold",
            "units_sold",
        ]
    )

    price_col = _find_column(
        df.columns,
        [
            "unit_price",
            "price",
            "selling_price",
            "sale_price",
            "unit_selling_price",
        ]
    )

    revenue_col = _find_column(
        df.columns,
        [
            "revenue",
            "sales",
            "sales_amount",
            "sales_value",
            "amount",
            "total_sales",
            "total_amount",
            "turnover",
            "net_sales",
        ]
    )

    # ========================================================
    # 2. REQUIRED FIELDS
    # ========================================================

    missing_columns = []

    if order_id_col is None:
        missing_columns.append("order_id / Order ID")

    if date_col is None:
        missing_columns.append("order_date / Order Date")

    if product_col is None:
        missing_columns.append("product_name / Product")

    if category_col is None:
        missing_columns.append("category / Category")

    if customer_col is None:
        missing_columns.append("customer_name / Customer")

    if region_col is None:
        missing_columns.append("region / Region")

    # Revenue can come directly from Excel OR be calculated
    # from Quantity × Price.
    if revenue_col is None and (
        quantity_col is None
        or price_col is None
    ):
        missing_columns.append(
            "revenue / sales / amount OR quantity + price"
        )

    if missing_columns:

        return None, missing_columns

    # ========================================================
    # 3. CREATE STANDARD DATAFRAME
    # ========================================================

    standard = pd.DataFrame()

    standard["order_id"] = df[order_id_col]

    standard["order_date"] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    standard["product_name"] = (
        df[product_col]
        .astype(str)
        .str.strip()
    )

    standard["category"] = (
        df[category_col]
        .astype(str)
        .str.strip()
    )

    standard["customer_name"] = (
        df[customer_col]
        .astype(str)
        .str.strip()
    )

    standard["region"] = (
        df[region_col]
        .astype(str)
        .str.strip()
    )

    # ========================================================
    # 4. QUANTITY
    # ========================================================

    if quantity_col is not None:

        standard["quantity"] = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        )

    else:

        # If Excel provides revenue only, treat every row
        # as one line item.
        standard["quantity"] = 1

    # ========================================================
    # 5. PRICE
    # ========================================================

    if price_col is not None:

        standard["price"] = pd.to_numeric(
            df[price_col],
            errors="coerce"
        )

    else:

        standard["price"] = pd.NA

    # ========================================================
    # 6. REVENUE
    # ========================================================

    if revenue_col is not None:

        standard["revenue"] = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        )

    else:

        standard["revenue"] = (
            standard["quantity"]
            * standard["price"]
        )

    # If price is absent but revenue exists, use revenue
    # as the displayed line-item price.
    standard["price"] = standard["price"].fillna(
        standard["revenue"]
    )

    # ========================================================
    # 7. CLEAN VALUES
    # ========================================================

    standard["quantity"] = (
        standard["quantity"]
        .fillna(1)
    )

    standard["revenue"] = (
        standard["revenue"]
        .fillna(
            standard["quantity"]
            * standard["price"]
        )
    )

    standard["price"] = (
        standard["price"]
        .fillna(0)
    )

    standard["customer_name"] = (
        standard["customer_name"]
        .replace(
            ["nan", "None", ""],
            "Unknown"
        )
    )

    standard["region"] = (
        standard["region"]
        .replace(
            ["nan", "None", ""],
            "Unknown"
        )
    )

    standard["category"] = (
        standard["category"]
        .replace(
            ["nan", "None", ""],
            "Unknown"
        )
    )

    # ========================================================
    # 8. REMOVE INVALID ROWS
    # ========================================================

    standard = standard[
        standard["order_id"].notna()
        & standard["order_date"].notna()
        & standard["product_name"].notna()
    ].copy()

    # ========================================================
    # 9. REMOVE EXACT DUPLICATES
    # ========================================================

    standard = (
        standard
        .drop_duplicates()
        .reset_index(drop=True)
    )

    if standard.empty:

        return (
            None,
            ["valid sales rows"]
        )

    # ========================================================
    # 10. CREATE ORDERS TABLE
    # ========================================================

    orders = (
        standard[
            [
                "order_id",
                "order_date",
                "customer_name",
                "region",
            ]
        ]
        .drop_duplicates(
            subset=["order_id"]
        )
        .copy()
    )

    orders["customer_id"] = (
        orders["customer_name"]
        .astype("category")
        .cat.codes
        + 1
    )

    # ========================================================
    # 11. CREATE ORDER ITEMS TABLE
    # ========================================================

    order_items = standard.copy()

    order_items["order_item_id"] = range(
        1,
        len(order_items) + 1
    )

    order_items["product_id"] = (
        order_items["product_name"]
        .astype("category")
        .cat.codes
        + 1
    )

    order_items = order_items[
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "product_name",
            "category",
            "price",
            "revenue",
        ]
    ].copy()

    return (
        orders,
        order_items
    ), []
