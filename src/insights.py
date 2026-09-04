# ============================================================
# AI BUSINESS ANALYST - BUSINESS INSIGHTS
# ============================================================

import pandas as pd


def generate_insights(
    total_revenue,
    total_orders,
    average_order_value,
    product_revenue,
    category_revenue,
    region_revenue,
    customer_revenue
):
    """
    Generate business insights from calculated analytics.

    Important:
    - Insights are based only on the supplied data.
    - No unsupported profit or margin claims are made.
    """

    insights = []

    # --------------------------------------------------------
    # 1. PRODUCT INSIGHT
    # --------------------------------------------------------

    if product_revenue is not None and not product_revenue.empty:

        top_product = product_revenue.idxmax()
        top_product_revenue = product_revenue.max()

        if total_revenue > 0:
            product_share = (
                top_product_revenue / total_revenue
            ) * 100
        else:
            product_share = 0

        insights.append(
            f"🏆 **Top Product:** {top_product} generated "
            f"₹{top_product_revenue:,.0f} in revenue, contributing "
            f"{product_share:.1f}% of total revenue."
        )

    # --------------------------------------------------------
    # 2. CATEGORY INSIGHT
    # --------------------------------------------------------

    if category_revenue is not None and not category_revenue.empty:

        top_category = category_revenue.idxmax()
        top_category_revenue = category_revenue.max()

        if total_revenue > 0:
            category_share = (
                top_category_revenue / total_revenue
            ) * 100
        else:
            category_share = 0

        insights.append(
            f"📦 **Top Category:** {top_category} generated "
            f"₹{top_category_revenue:,.0f} in revenue and accounts "
            f"for {category_share:.1f}% of total revenue."
        )

    # --------------------------------------------------------
    # 3. REGION INSIGHT
    # --------------------------------------------------------

    if region_revenue is not None and not region_revenue.empty:

        top_region = region_revenue.idxmax()
        top_region_revenue = region_revenue.max()

        if total_revenue > 0:
            region_share = (
                top_region_revenue / total_revenue
            ) * 100
        else:
            region_share = 0

        insights.append(
            f"🌍 **Top Region:** {top_region} generated "
            f"₹{top_region_revenue:,.0f} in revenue, representing "
            f"{region_share:.1f}% of total revenue."
        )

    # --------------------------------------------------------
    # 4. CUSTOMER INSIGHT
    # --------------------------------------------------------

    if customer_revenue is not None and not customer_revenue.empty:

        top_customer = customer_revenue.idxmax()
        top_customer_revenue = customer_revenue.max()

        insights.append(
            f"👑 **Highest-Value Customer:** {top_customer} generated "
            f"₹{top_customer_revenue:,.0f} in revenue."
        )

    # --------------------------------------------------------
    # 5. ORDER VALUE INSIGHT
    # --------------------------------------------------------

    if total_orders > 0:

        insights.append(
            f"🛒 **Order Performance:** The business processed "
            f"{total_orders:,} orders with an average order value "
            f"of ₹{average_order_value:,.0f}."
        )

    # --------------------------------------------------------
    # 6. REVENUE CONCENTRATION
    # --------------------------------------------------------

    if (
        product_revenue is not None
        and not product_revenue.empty
        and total_revenue > 0
    ):

        sorted_products = product_revenue.sort_values(
            ascending=False
        )

        if len(sorted_products) >= 2:

            top_two_revenue = sorted_products.iloc[:2].sum()

            top_two_share = (
                top_two_revenue / total_revenue
            ) * 100

            insights.append(
                f"📊 **Revenue Concentration:** The top two products "
                f"contribute {top_two_share:.1f}% of total revenue."
            )

    # --------------------------------------------------------
    # 7. BUSINESS RECOMMENDATION
    # --------------------------------------------------------

    recommendations = []

    # Product recommendation
    if product_revenue is not None and not product_revenue.empty:

        top_product = product_revenue.idxmax()

        recommendations.append(
            f"Focus inventory planning and sales efforts on "
            f"the strongest-performing product, {top_product}."
        )

    # Region recommendation
    if region_revenue is not None and not region_revenue.empty:

        top_region = region_revenue.idxmax()

        recommendations.append(
            f"Study the sales drivers in the {top_region} region "
            f"and evaluate whether successful practices can be "
            f"applied to weaker regions."
        )

    # Customer recommendation
    if customer_revenue is not None and not customer_revenue.empty:

        top_customer = customer_revenue.idxmax()

        recommendations.append(
            f"Maintain strong customer relationships with "
            f"{top_customer} while developing other high-potential "
            f"customers."
        )

    # --------------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------------

    if not insights:
        insights.append(
            "The available business data is not sufficient "
            "to generate meaningful insights."
        )

    return {
        "insights": insights,
        "recommendations": recommendations
    }