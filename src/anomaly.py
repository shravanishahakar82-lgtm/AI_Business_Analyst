import pandas as pd


def detect_anomalies(monthly_revenue):
    """
    Detect unusual changes in monthly revenue.
    """

    anomalies = []

    if len(monthly_revenue) < 2:
        return anomalies

    revenue_values = monthly_revenue.values

    for i in range(1, len(revenue_values)):

        previous_revenue = revenue_values[i - 1]
        current_revenue = revenue_values[i]

        if previous_revenue == 0:
            continue

        percentage_change = (
            (current_revenue - previous_revenue)
            / previous_revenue
        ) * 100

        current_month = monthly_revenue.index[i]

        # Revenue dropped by more than 20%
        if percentage_change <= -20:

            anomalies.append(
                f"⚠️ Revenue dropped by {abs(percentage_change):.1f}% "
                f"in {current_month} compared with the previous month."
            )

        # Revenue increased by more than 30%
        elif percentage_change >= 30:

            anomalies.append(
                f"🚀 Revenue increased by {percentage_change:.1f}% "
                f"in {current_month} compared with the previous month."
            )

    return anomalies