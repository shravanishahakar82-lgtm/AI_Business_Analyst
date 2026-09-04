import pandas as pd


# ============================================================
# AI BUSINESS ANALYST
# ADVANCED BUSINESS ANALYSIS ENGINE
# ============================================================


def prepare_data(df):
    """
    Prepare and standardize business data before analysis.
    """

    data = df.copy()

    # --------------------------------------------------------
    # Standardize column names
    # --------------------------------------------------------
    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------------------------
    # Convert date column
    # --------------------------------------------------------
    if "order_date" in data.columns:
        data["order_date"] = pd.to_datetime(
            data["order_date"],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Convert numeric columns
    # --------------------------------------------------------
    numeric_columns = [
        "quantity",
        "price",
        "revenue",
        "cost",
        "cost_price",
        "cogs",
        "profit"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    # --------------------------------------------------------
    # Calculate revenue if missing
    # --------------------------------------------------------
    if "revenue" not in data.columns:

        if "quantity" in data.columns and "price" in data.columns:

            data["revenue"] = (
                data["quantity"].fillna(0)
                * data["price"].fillna(0)
            )

    # --------------------------------------------------------
    # Fill optional text columns
    # --------------------------------------------------------
    text_columns = [
        "product_name",
        "category",
        "customer_name",
        "region"
    ]

    for column in text_columns:
        if column in data.columns:
            data[column] = (
                data[column]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

    return data


# ============================================================
# CORE KPIs
# ============================================================


def get_total_revenue(df):
    """Return total business revenue."""

    if "revenue" not in df.columns:
        return 0

    return df["revenue"].fillna(0).sum()


def get_total_orders(df):
    """Return number of unique orders."""

    if "order_id" in df.columns:
        return df["order_id"].nunique()

    return len(df)


def get_average_order_value(df):
    """Calculate Average Order Value."""

    total_revenue = get_total_revenue(df)
    total_orders = get_total_orders(df)

    if total_orders == 0:
        return 0

    return total_revenue / total_orders


# ============================================================
# MONTHLY ANALYSIS
# ============================================================


def get_monthly_revenue(df):
    """
    Calculate monthly revenue.
    """

    data = df.copy()

    if "order_date" not in data.columns:
        return pd.Series(dtype=float)

    data["order_date"] = pd.to_datetime(
        data["order_date"],
        errors="coerce"
    )

    data = data.dropna(subset=["order_date"])

    if data.empty:
        return pd.Series(dtype=float)

    monthly = (
        data.groupby(
            data["order_date"].dt.to_period("M")
        )["revenue"]
        .sum()
    )

    monthly.index = monthly.index.astype(str)

    return monthly


def get_monthly_growth(df):
    """
    Calculate Month-over-Month revenue growth.
    """

    monthly = get_monthly_revenue(df)

    if len(monthly) < 2:
        return pd.DataFrame(
            columns=[
                "month",
                "revenue",
                "previous_revenue",
                "growth_percent"
            ]
        )

    result = pd.DataFrame({
        "month": monthly.index,
        "revenue": monthly.values
    })

    result["previous_revenue"] = result["revenue"].shift(1)

    result["growth_percent"] = (
        (
            result["revenue"]
            - result["previous_revenue"]
        )
        / result["previous_revenue"]
        * 100
    )

    result["growth_percent"] = (
        result["growth_percent"]
        .replace([float("inf"), -float("inf")], pd.NA)
        .round(2)
    )

    return result


def get_best_month(df):
    """
    Return month with highest revenue.
    """

    monthly = get_monthly_revenue(df)

    if monthly.empty:
        return None, 0

    month = monthly.idxmax()
    revenue = monthly.max()

    return month, revenue


def get_worst_month(df):
    """
    Return month with lowest revenue.
    """

    monthly = get_monthly_revenue(df)

    if monthly.empty:
        return None, 0

    month = monthly.idxmin()
    revenue = monthly.min()

    return month, revenue


# ============================================================
# PRODUCT ANALYSIS
# ============================================================


def get_product_revenue(df):
    """Calculate revenue by product."""

    if "product_name" not in df.columns:
        return pd.Series(dtype=float)

    return (
        df.groupby("product_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )


def get_product_analysis(df):
    """
    Detailed product performance analysis.
    """

    if "product_name" not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby("product_name")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique")
            if "order_id" in df.columns
            else ("revenue", "count"),
            quantity=("quantity", "sum")
            if "quantity" in df.columns
            else ("revenue", "count")
        )
        .sort_values("revenue", ascending=False)
    )

    total_revenue = result["revenue"].sum()

    if total_revenue > 0:
        result["revenue_share_percent"] = (
            result["revenue"]
            / total_revenue
            * 100
        ).round(2)
    else:
        result["revenue_share_percent"] = 0

    result["rank"] = (
        result["revenue"]
        .rank(
            method="dense",
            ascending=False
        )
        .astype(int)
    )

    return result


def get_top_product(df):
    """Return highest revenue product."""

    product_revenue = get_product_revenue(df)

    if product_revenue.empty:
        return "N/A", 0

    return (
        product_revenue.idxmax(),
        product_revenue.max()
    )


def get_bottom_product(df):
    """Return lowest revenue product."""

    product_revenue = get_product_revenue(df)

    if product_revenue.empty:
        return "N/A", 0

    return (
        product_revenue.idxmin(),
        product_revenue.min()
    )


# ============================================================
# CATEGORY ANALYSIS
# ============================================================


def get_category_revenue(df):
    """Calculate revenue by category."""

    if "category" not in df.columns:
        return pd.Series(dtype=float)

    return (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )


def get_category_analysis(df):
    """
    Detailed category performance.
    """

    category_revenue = get_category_revenue(df)

    if category_revenue.empty:
        return pd.DataFrame()

    result = category_revenue.to_frame(
        name="revenue"
    )

    total_revenue = result["revenue"].sum()

    if total_revenue > 0:
        result["revenue_share_percent"] = (
            result["revenue"]
            / total_revenue
            * 100
        ).round(2)
    else:
        result["revenue_share_percent"] = 0

    result["rank"] = (
        result["revenue"]
        .rank(
            method="dense",
            ascending=False
        )
        .astype(int)
    )

    return result


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================


def get_customer_revenue(df):
    """Calculate revenue by customer."""

    if "customer_name" not in df.columns:
        return pd.Series(dtype=float)

    return (
        df.groupby("customer_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )


def get_customer_analysis(df):
    """
    Detailed customer performance.
    """

    if "customer_name" not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby("customer_name")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique")
            if "order_id" in df.columns
            else ("revenue", "count")
        )
        .sort_values("revenue", ascending=False)
    )

    result["average_order_value"] = (
        result["revenue"]
        / result["orders"]
    ).round(2)

    result["rank"] = (
        result["revenue"]
        .rank(
            method="dense",
            ascending=False
        )
        .astype(int)
    )

    return result


def get_top_customer(df):
    """Return highest-value customer."""

    customer_revenue = get_customer_revenue(df)

    if customer_revenue.empty:
        return "N/A", 0

    return (
        customer_revenue.idxmax(),
        customer_revenue.max()
    )


# ============================================================
# REGION ANALYSIS
# ============================================================


def get_region_revenue(df):
    """Calculate revenue by region."""

    if "region" not in df.columns:
        return pd.Series(dtype=float)

    return (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )


def get_region_analysis(df):
    """
    Detailed regional performance.
    """

    region_revenue = get_region_revenue(df)

    if region_revenue.empty:
        return pd.DataFrame()

    result = region_revenue.to_frame(
        name="revenue"
    )

    total_revenue = result["revenue"].sum()

    if total_revenue > 0:
        result["revenue_share_percent"] = (
            result["revenue"]
            / total_revenue
            * 100
        ).round(2)
    else:
        result["revenue_share_percent"] = 0

    result["rank"] = (
        result["revenue"]
        .rank(
            method="dense",
            ascending=False
        )
        .astype(int)
    )

    return result


def get_top_region(df):
    """Return highest revenue region."""

    region_revenue = get_region_revenue(df)

    if region_revenue.empty:
        return "N/A", 0

    return (
        region_revenue.idxmax(),
        region_revenue.max()
    )


# ============================================================
# REVENUE CONCENTRATION
# ============================================================


def get_revenue_concentration(df):
    """
    Determine how much revenue comes from the
    top-performing product.
    """

    product_revenue = get_product_revenue(df)

    total_revenue = get_total_revenue(df)

    if product_revenue.empty or total_revenue == 0:
        return 0

    return round(
        product_revenue.iloc[0]
        / total_revenue
        * 100,
        2
    )


# ============================================================
# PROFIT ANALYSIS
# ============================================================


def get_profit_analysis(df):
    """
    Calculate profit only when cost information
    exists in the uploaded data.

    We NEVER estimate profit from revenue.
    """

    data = df.copy()

    cost_column = None

    for column in ["cost", "cost_price", "cogs"]:
        if column in data.columns:
            cost_column = column
            break

    if cost_column is None:
        return {
            "available": False,
            "total_profit": None,
            "profit_margin": None,
            "message": (
                "Profit analysis is unavailable because "
                "the dataset does not contain cost/COGS data."
            )
        }

    data[cost_column] = pd.to_numeric(
        data[cost_column],
        errors="coerce"
    )

    data["calculated_profit"] = (
        data["revenue"] - data[cost_column]
    )

    total_revenue = data["revenue"].sum()
    total_profit = data["calculated_profit"].sum()

    if total_revenue > 0:
        profit_margin = (
            total_profit
            / total_revenue
            * 100
        )
    else:
        profit_margin = 0

    return {
        "available": True,
        "total_profit": total_profit,
        "profit_margin": round(profit_margin, 2),
        "message": "Profit analysis calculated from available cost data."
    }


# ============================================================
# BUSINESS SUMMARY
# ============================================================


def generate_business_summary(df):
    """
    Generate a structured business summary that can be
    passed to the AI assistant.
    """

    data = prepare_data(df)

    total_revenue = get_total_revenue(data)
    total_orders = get_total_orders(data)
    average_order_value = get_average_order_value(data)

    top_product, top_product_revenue = get_top_product(data)
    bottom_product, bottom_product_revenue = get_bottom_product(data)

    top_customer, top_customer_revenue = get_top_customer(data)

    top_region, top_region_revenue = get_top_region(data)

    best_month, best_month_revenue = get_best_month(data)
    worst_month, worst_month_revenue = get_worst_month(data)

    concentration = get_revenue_concentration(data)

    profit = get_profit_analysis(data)

    summary = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value": average_order_value,

        "top_product": top_product,
        "top_product_revenue": top_product_revenue,

        "bottom_product": bottom_product,
        "bottom_product_revenue": bottom_product_revenue,

        "top_customer": top_customer,
        "top_customer_revenue": top_customer_revenue,

        "top_region": top_region,
        "top_region_revenue": top_region_revenue,

        "best_month": best_month,
        "best_month_revenue": best_month_revenue,

        "worst_month": worst_month,
        "worst_month_revenue": worst_month_revenue,

        "top_product_revenue_share": concentration,

        "profit_available": profit["available"],
        "total_profit": profit["total_profit"],
        "profit_margin": profit["profit_margin"]
    }

    return summary


# ============================================================
# COMPLETE ANALYSIS FUNCTION
# ============================================================


def analyze_business_data(df):
    """
    Main analysis function.

    Returns all important business-analysis outputs
    in one dictionary.
    """

    data = prepare_data(df)

    return {
        "data": data,

        "total_revenue": get_total_revenue(data),
        "total_orders": get_total_orders(data),
        "average_order_value": get_average_order_value(data),

        "monthly_revenue": get_monthly_revenue(data),
        "monthly_growth": get_monthly_growth(data),

        "product_revenue": get_product_revenue(data),
        "product_analysis": get_product_analysis(data),

        "category_revenue": get_category_revenue(data),
        "category_analysis": get_category_analysis(data),

        "customer_revenue": get_customer_revenue(data),
        "customer_analysis": get_customer_analysis(data),

        "region_revenue": get_region_revenue(data),
        "region_analysis": get_region_analysis(data),

        "top_product": get_top_product(data),
        "bottom_product": get_bottom_product(data),

        "top_customer": get_top_customer(data),
        "top_region": get_top_region(data),

        "best_month": get_best_month(data),
        "worst_month": get_worst_month(data),

        "revenue_concentration": get_revenue_concentration(data),

        "profit_analysis": get_profit_analysis(data),

        "business_summary": generate_business_summary(data)
    }


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================
# These aliases help prevent older dashboard code from
# breaking if it uses the earlier function names.


def analyze_data(df):
    return analyze_business_data(df)