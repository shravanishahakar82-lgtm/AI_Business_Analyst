import streamlit as st
import sqlite3
import pandas as pd
import io

from analysis import analyze_business_data
from insights import generate_insights
from anomaly import detect_anomalies
from ai_assistant import ask_ai

from excel_loader import (
    load_excel_file,
    validate_business_data,
    prepare_excel_data
)

from visualization import (
    monthly_revenue_chart,
    product_revenue_chart,
    category_revenue_chart,
    region_revenue_chart,
    customer_revenue_chart
)


# ============================================================
# AI BUSINESS ANALYST DASHBOARD
# Excel + SQLite + Pandas + Plotly + Ollama
# ============================================================

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def build_business_dataframe(orders_df, items_df):
    """Create one standard sales dataframe for analysis."""

    order_columns = [
        "order_id",
        "customer_name",
        "region",
        "order_date"
    ]

    available_order_columns = [
        c for c in order_columns if c in orders_df.columns
    ]

    business_df = items_df.merge(
        orders_df[available_order_columns].drop_duplicates("order_id"),
        on="order_id",
        how="left"
    )

    # Standardize types
    if "order_date" in business_df.columns:
        business_df["order_date"] = pd.to_datetime(
            business_df["order_date"],
            errors="coerce"
        )

    for column in ["quantity", "price", "revenue"]:
        if column in business_df.columns:
            business_df[column] = pd.to_numeric(
                business_df[column],
                errors="coerce"
            ).fillna(0)

    # Standardize text
    for column in [
        "product_name",
        "category",
        "customer_name",
        "region"
    ]:
        if column in business_df.columns:
            business_df[column] = (
                business_df[column]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

    # Revenue fallback
    if "revenue" not in business_df.columns:
        if "quantity" in business_df.columns and "price" in business_df.columns:
            business_df["revenue"] = (
                business_df["quantity"] * business_df["price"]
            )

    return business_df


def create_excel_download(dataframe):
    """Create an Excel file in memory."""

    buffer = io.BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Filtered Sales"
        )

    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# SIDEBAR - DATA SOURCE
# ============================================================

st.sidebar.header("📂 Data Source")

data_source = st.sidebar.radio(
    "Choose data source",
    [
        "Sample Database",
        "Upload Excel"
    ]
)


orders = None
order_items = None
excel_df = None


# ============================================================
# SAMPLE DATABASE
# ============================================================

if data_source == "Sample Database":

    st.sidebar.success("✅ Sample database loaded")

    connection = sqlite3.connect(
        "data/business.db"
    )

    orders = pd.read_sql_query(
        """
        SELECT
            orders.order_id,
            orders.customer_id,
            orders.order_date,
            customers.customer_name,
            customers.region
        FROM orders
        JOIN customers
        ON orders.customer_id = customers.customer_id
        """,
        connection
    )

    order_items = pd.read_sql_query(
        """
        SELECT
            order_items.order_item_id,
            order_items.order_id,
            order_items.product_id,
            order_items.quantity,
            products.product_name,
            products.category,
            products.price
        FROM order_items
        JOIN products
        ON order_items.product_id = products.product_id
        """,
        connection
    )

    connection.close()

    order_items["revenue"] = (
        order_items["quantity"] * order_items["price"]
    )


# ============================================================
# EXCEL UPLOAD
# ============================================================

else:

    st.sidebar.subheader("📤 Upload Excel file")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel file",
        type=["xlsx", "xls"]
    )

    st.sidebar.caption(
        "Excel can contain multiple sheets. "
        "The application automatically searches for "
        "the sales-data sheet."
    )

    if uploaded_file is None:

        st.title("📊 AI Business Analyst")

        st.info(
            "Please upload an Excel file to continue."
        )

        st.stop()

    try:

        excel_df = load_excel_file(uploaded_file)

        valid, validation_message = validate_business_data(
            excel_df
        )

        if not valid:
            st.error(validation_message)
            st.stop()

        prepared_data, missing_columns = prepare_excel_data(
            excel_df
        )

        if prepared_data is None:

            st.error(
                "Excel file is missing required business columns."
            )

            st.write("Missing:")

            for column in missing_columns:
                st.write(f"- {column}")

            st.stop()

        orders, order_items = prepared_data

        source_sheet = excel_df.attrs.get(
            "source_sheet",
            "Sales Data"
        )

        st.sidebar.success(
            f"✅ Loaded {len(excel_df)} Excel rows"
        )

        st.sidebar.caption(
            f"Sales sheet: {source_sheet}"
        )

    except Exception as e:

        st.error(
            f"❌ Could not load Excel file: {e}"
        )

        st.stop()


# ============================================================
# STANDARD BUSINESS DATA
# ============================================================

business_df = build_business_dataframe(
    orders,
    order_items
)

business_df = business_df[
    business_df["order_date"].notna()
].copy()


if business_df.empty:

    st.error(
        "❌ No valid business records are available."
    )

    st.stop()


# ============================================================
# EXCEL DATA QUALITY
# ============================================================

if data_source == "Upload Excel":

    st.sidebar.divider()
    st.sidebar.header("📋 Data Quality")

    rows_loaded = len(excel_df)

    duplicate_rows = int(
        excel_df.duplicated().sum()
    )

    required_columns = [
        "order_id",
        "order_date",
        "product_name",
        "category",
        "quantity",
        "price",
        "revenue",
        "customer_name",
        "region"
    ]

    available_columns = [
        c for c in required_columns
        if c in excel_df.columns
    ]

    missing_values = int(
        excel_df[available_columns]
        .isna()
        .sum()
        .sum()
    ) if available_columns else 0

    invalid_dates = 0

    if "order_date" in excel_df.columns:

        converted_dates = pd.to_datetime(
            excel_df["order_date"],
            errors="coerce"
        )

        invalid_dates = int(
            converted_dates.isna().sum()
        )

    invalid_revenue = 0

    if "revenue" in excel_df.columns:

        revenue_values = pd.to_numeric(
            excel_df["revenue"],
            errors="coerce"
        )

        invalid_revenue = int(
            revenue_values.isna().sum()
        )

    clean_rows = max(
        rows_loaded - duplicate_rows,
        0
    )

    if (
        duplicate_rows == 0
        and missing_values == 0
        and invalid_dates == 0
        and invalid_revenue == 0
    ):
        quality_status = "🟢 Good"

    elif (
        duplicate_rows <= 5
        and invalid_dates <= 2
        and invalid_revenue <= 2
    ):
        quality_status = "🟡 Review"

    else:
        quality_status = "🔴 Needs Cleaning"

    st.sidebar.metric(
        "Rows Loaded",
        rows_loaded
    )

    st.sidebar.metric(
        "Duplicate Rows",
        duplicate_rows
    )

    st.sidebar.metric(
        "Missing Values",
        missing_values
    )

    st.sidebar.metric(
        "Data Quality",
        quality_status
    )

    st.divider()

    st.header("📋 Excel Data Quality")

    st.write(
        "Data validation performed before business analysis."
    )

    q1, q2, q3, q4, q5 = st.columns(5)

    q1.metric("Rows Loaded", rows_loaded)
    q2.metric("Duplicate Rows", duplicate_rows)
    q3.metric("Missing Values", missing_values)
    q4.metric("Invalid Dates", invalid_dates)
    q5.metric("Invalid Revenue", invalid_revenue)

    if quality_status == "🟢 Good":

        st.success(
            f"✅ Data quality check completed. "
            f"{clean_rows} rows are ready for analysis."
        )

    elif quality_status == "🟡 Review":

        st.warning(
            "⚠️ The Excel file contains a few "
            "data-quality issues that should be reviewed."
        )

    else:

        st.error(
            "❌ The Excel file contains significant "
            "data-quality issues."
        )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.divider()
st.sidebar.header("🔎 Filters")

if st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True
):

    for key in [
        "selected_region",
        "selected_category",
        "selected_product",
        "selected_customer"
    ]:

        if key in st.session_state:
            del st.session_state[key]

    st.rerun()


minimum_date = business_df["order_date"].min().date()
maximum_date = business_df["order_date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Select Date Range",
    value=(minimum_date, maximum_date)
)


region_options = ["All"] + sorted(
    business_df["region"].unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "🌍 Select Region",
    region_options,
    key="selected_region"
)


customer_options = ["All"] + sorted(
    business_df["customer_name"].unique().tolist()
)

selected_customer = st.sidebar.selectbox(
    "👤 Select Customer",
    customer_options,
    key="selected_customer"
)


category_options = ["All"] + sorted(
    business_df["category"].unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "🏷️ Select Category",
    category_options,
    key="selected_category"
)


product_options = ["All"] + sorted(
    business_df["product_name"].unique().tolist()
)

selected_product = st.sidebar.selectbox(
    "📦 Select Product",
    product_options,
    key="selected_product"
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_data = business_df.copy()


if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.to_datetime(selected_dates[0])
    end_date = (
        pd.to_datetime(selected_dates[1])
        + pd.Timedelta(days=1)
    )

    filtered_data = filtered_data[
        (filtered_data["order_date"] >= start_date)
        & (filtered_data["order_date"] < end_date)
    ].copy()


if selected_region != "All":

    filtered_data = filtered_data[
        filtered_data["region"] == selected_region
    ].copy()


if selected_customer != "All":

    filtered_data = filtered_data[
        filtered_data["customer_name"] == selected_customer
    ].copy()


if selected_category != "All":

    filtered_data = filtered_data[
        filtered_data["category"] == selected_category
    ].copy()


if selected_product != "All":

    filtered_data = filtered_data[
        filtered_data["product_name"] == selected_product
    ].copy()


# ============================================================
# ACTIVE FILTERS
# ============================================================

st.sidebar.divider()
st.sidebar.subheader("📌 Active Filters")

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    st.sidebar.caption(
        f"📅 {selected_dates[0]} → {selected_dates[1]}"
    )

if selected_region != "All":
    st.sidebar.caption(
        f"🌍 Region: {selected_region}"
    )

if selected_customer != "All":
    st.sidebar.caption(
        f"👤 Customer: {selected_customer}"
    )

if selected_category != "All":
    st.sidebar.caption(
        f"🏷️ Category: {selected_category}"
    )

if selected_product != "All":
    st.sidebar.caption(
        f"📦 Product: {selected_product}"
    )


# ============================================================
# EMPTY RESULT CHECK
# ============================================================

if filtered_data.empty:

    st.title("📊 AI Business Analyst Dashboard")

    st.warning(
        "⚠️ No business data found for the selected filters."
    )

    st.info(
        "Try changing the Date, Region, Customer, "
        "Category or Product filter."
    )

    st.stop()


# ============================================================
# CENTRAL ANALYSIS ENGINE
# ============================================================

analysis = analyze_business_data(
    filtered_data
)

total_revenue = analysis["total_revenue"]
total_orders = analysis["total_orders"]
average_order_value = analysis["average_order_value"]

monthly_revenue = analysis["monthly_revenue"]

product_revenue = analysis["product_revenue"]
category_revenue = analysis["category_revenue"]
region_revenue = analysis["region_revenue"]
customer_revenue = analysis["customer_revenue"]

top_product, top_product_revenue = analysis["top_product"]
bottom_product, bottom_product_revenue = analysis["bottom_product"]

top_customer, top_customer_revenue = analysis["top_customer"]
top_region, top_region_revenue = analysis["top_region"]

top_category = (
    str(category_revenue.index[0])
    if not category_revenue.empty
    else "N/A"
)

best_month, best_month_revenue = analysis["best_month"]
worst_month, worst_month_revenue = analysis["worst_month"]

revenue_concentration = analysis[
    "revenue_concentration"
]

profit_analysis = analysis[
    "profit_analysis"
]


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title(
    "📊 AI Business Analyst Dashboard"
)

st.markdown(
    "### Business Performance Overview"
)

st.caption(
    f"Showing {total_orders} orders and "
    f"₹{total_revenue:,.0f} revenue based on current filters."
)

st.divider()


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "💰 Total Revenue",
    f"₹{total_revenue:,.0f}"
)

c2.metric(
    "🛒 Total Orders",
    total_orders
)

c3.metric(
    "📦 Average Order Value",
    f"₹{average_order_value:,.0f}"
)

c4.metric(
    "🏆 Top Product",
    top_product
)

c5.metric(
    "👑 Top Customer",
    top_customer
)


# ============================================================
# ADVANCED BUSINESS ANALYSIS
# ============================================================

st.divider()

st.header("📊 Advanced Business Analysis")

a1, a2, a3, a4 = st.columns(4)

with a1:
    st.metric(
        "🏆 Best Month",
        best_month if best_month else "N/A"
    )
    if best_month:
        st.caption(
            f"Revenue: ₹{best_month_revenue:,.0f}"
        )

with a2:
    st.metric(
        "📉 Lowest Month",
        worst_month if worst_month else "N/A"
    )
    if worst_month:
        st.caption(
            f"Revenue: ₹{worst_month_revenue:,.0f}"
        )

with a3:
    st.metric(
        "🌍 Best Region",
        top_region
    )
    st.caption(
        f"Revenue: ₹{top_region_revenue:,.0f}"
    )

with a4:
    st.metric(
        "🏷️ Best Category",
        top_category
    )

st.write("")

b1, b2, b3, b4 = st.columns(4)

b1.metric(
    "🥇 Top Product Revenue",
    f"₹{top_product_revenue:,.0f}"
)

b2.metric(
    "📌 Top Product Share",
    f"{revenue_concentration:.1f}%"
)

b3.metric(
    "👤 Top Customer Revenue",
    f"₹{top_customer_revenue:,.0f}"
)

if profit_analysis["available"]:

    b4.metric(
        "💰 Profit Margin",
        f"{profit_analysis['profit_margin']:.1f}%"
    )

else:

    b4.metric(
        "💰 Profit Analysis",
        "Not Available"
    )


# ============================================================
# MONTHLY REVENUE
# ============================================================

st.divider()

st.header("📈 Monthly Revenue")

if not monthly_revenue.empty:

    st.plotly_chart(
        monthly_revenue_chart(monthly_revenue),
        use_container_width=True
    )


# ============================================================
# MONTH-OVER-MONTH ANALYSIS
# ============================================================

monthly_growth = analysis["monthly_growth"]

if not monthly_growth.empty:

    st.subheader("📊 Month-over-Month Growth")

    growth_display = monthly_growth.copy()

    growth_display["revenue"] = (
        growth_display["revenue"]
        .map(lambda x: f"₹{x:,.0f}")
    )

    growth_display["previous_revenue"] = (
        growth_display["previous_revenue"]
        .map(
            lambda x:
            "—" if pd.isna(x)
            else f"₹{x:,.0f}"
        )
    )

    growth_display["growth_percent"] = (
        growth_display["growth_percent"]
        .map(
            lambda x:
            "—" if pd.isna(x)
            else f"{x:.2f}%"
        )
    )

    st.dataframe(
        growth_display,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PRODUCT + CATEGORY
# ============================================================

st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.header("📦 Product-wise Revenue")

    st.plotly_chart(
        product_revenue_chart(product_revenue),
        use_container_width=True
    )


with chart_col2:

    st.header("🏷️ Category-wise Revenue")

    st.plotly_chart(
        category_revenue_chart(category_revenue),
        use_container_width=True
    )


# ============================================================
# REGION
# ============================================================

st.header("🌍 Region-wise Revenue")

st.plotly_chart(
    region_revenue_chart(region_revenue),
    use_container_width=True
)


# ============================================================
# CUSTOMER
# ============================================================

st.header("👥 Customer-wise Revenue")

st.plotly_chart(
    customer_revenue_chart(customer_revenue),
    use_container_width=True
)


# ============================================================
# ANALYSIS TABLES
# ============================================================

st.divider()

st.header("📋 Business Analysis Tables")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏆 Products",
        "👥 Customers",
        "🌍 Regions",
        "🏷️ Categories"
    ]
)


with tab1:

    product_analysis = analysis["product_analysis"]

    if not product_analysis.empty:

        st.dataframe(
            product_analysis.reset_index(),
            use_container_width=True
        )


with tab2:

    customer_analysis = analysis["customer_analysis"]

    if not customer_analysis.empty:

        st.dataframe(
            customer_analysis.reset_index(),
            use_container_width=True
        )


with tab3:

    region_analysis = analysis["region_analysis"]

    if not region_analysis.empty:

        st.dataframe(
            region_analysis.reset_index(),
            use_container_width=True
        )


with tab4:

    category_analysis = analysis["category_analysis"]

    if not category_analysis.empty:

        st.dataframe(
            category_analysis.reset_index(),
            use_container_width=True
        )


# ============================================================
# FILTERED DATA PREVIEW
# ============================================================

st.divider()

st.header("🔍 Filtered Sales Data")

display_columns = [
    "order_id",
    "customer_name",
    "region",
    "order_date",
    "product_name",
    "category",
    "quantity",
    "price",
    "revenue"
]

available_display_columns = [
    c for c in display_columns
    if c in filtered_data.columns
]

display_data = filtered_data[
    available_display_columns
].copy()

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EXPORT FILTERED DATA
# ============================================================

st.header("📥 Export Filtered Data")

st.caption(
    "Download the currently filtered business data "
    "for further analysis in Excel or other tools."
)

csv_data = display_data.to_csv(
    index=False
).encode("utf-8")

excel_data = create_excel_download(
    display_data
)

d1, d2 = st.columns(2)

with d1:

    st.download_button(
        label="📄 Download CSV",
        data=csv_data,
        file_name="filtered_business_data.csv",
        mime="text/csv",
        use_container_width=True
    )

with d2:

    st.download_button(
        label="📊 Download Excel",
        data=excel_data,
        file_name="filtered_business_data.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )


# ============================================================
# ANOMALY DETECTION
# ============================================================

st.divider()

st.header("🚨 Business Risk & Anomaly Detection")

anomalies = detect_anomalies(
    monthly_revenue
)

if anomalies:

    for anomaly in anomalies:
        st.warning(anomaly)

else:

    st.success(
        "✅ No significant revenue anomalies detected."
    )


# ============================================================
# RULE-BASED BUSINESS INSIGHTS
# ============================================================

st.divider()

st.header("💡 Business Insights")

try:

    insight_result = generate_insights(
        total_revenue,
        total_orders,
        average_order_value,
        product_revenue,
        category_revenue,
        region_revenue,
        customer_revenue
    )

    # insights.py returns a dictionary containing:
    # "insights" and "recommendations"

    if isinstance(insight_result, dict):

        business_insights = insight_result.get("insights", [])
        recommendations = insight_result.get("recommendations", [])

        if business_insights:

            st.subheader("📊 Key Findings")

            for insight in business_insights:
                st.markdown(insight)

        else:

            st.info(
                "No additional business insights are available."
            )

        if recommendations:

            st.subheader("💡 Recommendations")

            for recommendation in recommendations:
                st.markdown(f"• {recommendation}")

    else:

        # Backward compatibility if insights.py returns a list.
        if insight_result:

            for insight in insight_result:
                st.markdown(insight)

        else:

            st.info(
                "No additional business insights are available."
            )

except Exception as e:

    st.warning(
        f"Business insights could not be generated: {e}"
    )


# ============================================================
# AI BUSINESS ASSISTANT
# ============================================================

st.divider()

st.header("🤖 Ask AI — Business Analyst")

st.write(
    "Ask a question about the currently filtered "
    "business data."
)


# Build a controlled data summary for Ollama.
# This prevents the AI from needing the entire raw dataset.

business_data = f"""
BUSINESS PERFORMANCE

Total Revenue: ₹{total_revenue:,.0f}
Total Orders: {total_orders}
Average Order Value: ₹{average_order_value:,.0f}

CURRENT FILTERS

Region: {selected_region}
Customer: {selected_customer}
Category: {selected_category}
Product: {selected_product}

TOP PERFORMERS

Top Product: {top_product}
Top Product Revenue: ₹{top_product_revenue:,.0f}

Top Category: {top_category}

Top Region: {top_region}
Top Region Revenue: ₹{top_region_revenue:,.0f}

Top Customer: {top_customer}
Top Customer Revenue: ₹{top_customer_revenue:,.0f}

Best Month: {best_month}
Best Month Revenue: ₹{best_month_revenue:,.0f}

Worst Month: {worst_month}
Worst Month Revenue: ₹{worst_month_revenue:,.0f}

Top Product Revenue Share: {revenue_concentration:.2f}%

PRODUCT REVENUE
{product_revenue.to_string()}

CATEGORY REVENUE
{category_revenue.to_string()}

REGION REVENUE
{region_revenue.to_string()}

CUSTOMER REVENUE
{customer_revenue.to_string()}

MONTHLY REVENUE
{monthly_revenue.to_string()}

ANOMALIES
{
    chr(10).join(anomalies)
    if anomalies
    else "No significant revenue anomalies detected."
}

PROFIT INFORMATION
{
    profit_analysis["message"]
    if not profit_analysis["available"]
    else f"Total Profit: ₹{profit_analysis['total_profit']:,.0f}; "
         f"Profit Margin: {profit_analysis['profit_margin']:.2f}%"
}
"""


question = st.text_input(
    "💬 Ask a business question",
    placeholder=(
        "Example: Which product is performing best?"
    )
)


if st.button(
    "🤖 Ask AI",
    type="primary"
):

    if not question.strip():

        st.warning(
            "Please enter a business question first."
        )

    else:

        with st.spinner(
            "🤖 AI is analyzing the filtered business data..."
        ):

            try:

                answer = ask_ai(
                    question,
                    business_data
                )

                st.subheader(
                    "💡 AI Recommendation"
                )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    "Unable to get an AI response."
                )

                st.caption(
                    f"Technical details: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Business Analyst | "
    "Python • Pandas • SQLite • Excel • "
    "Plotly • Streamlit • Ollama"
)
