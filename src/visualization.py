import plotly.express as px


# ==========================================
# MONTHLY REVENUE CHART
# ==========================================

def monthly_revenue_chart(monthly_revenue):

    data = monthly_revenue.reset_index()

    data.columns = ["month", "revenue"]

    fig = px.line(
        data,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
        hovermode="x unified"
    )

    return fig


# ==========================================
# PRODUCT REVENUE CHART
# ==========================================

def product_revenue_chart(product_revenue):

    data = product_revenue.reset_index()

    data.columns = ["product", "revenue"]

    fig = px.bar(
        data,
        x="product",
        y="revenue",
        title="Product-wise Revenue",
        text="revenue"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Revenue (₹)"
    )

    return fig


# ==========================================
# CATEGORY REVENUE CHART
# ==========================================

def category_revenue_chart(category_revenue):

    data = category_revenue.reset_index()

    data.columns = ["category", "revenue"]

    fig = px.pie(
        data,
        names="category",
        values="revenue",
        title="Category-wise Revenue"
    )

    return fig


# ==========================================
# REGION REVENUE CHART
# ==========================================

def region_revenue_chart(region_revenue):

    data = region_revenue.reset_index()

    data.columns = ["region", "revenue"]

    fig = px.bar(
        data,
        x="region",
        y="revenue",
        title="Region-wise Revenue",
        text="revenue"
    )

    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Revenue (₹)"
    )

    return fig


# ==========================================
# CUSTOMER REVENUE CHART
# ==========================================

def customer_revenue_chart(customer_revenue):

    data = customer_revenue.reset_index()

    data.columns = ["customer", "revenue"]

    fig = px.bar(
        data,
        x="customer",
        y="revenue",
        title="Customer-wise Revenue",
        text="revenue"
    )

    fig.update_layout(
        xaxis_title="Customer",
        yaxis_title="Revenue (₹)"
    )

    return fig