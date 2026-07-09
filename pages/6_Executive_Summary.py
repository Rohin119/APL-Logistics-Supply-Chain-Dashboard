import streamlit as st
import plotly.express as px
from utils import load_data, calculate_kpis

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📊",
    layout="wide"
)

df = load_data()

kpi = calculate_kpis(df)

st.title("📊 Executive Summary")

st.markdown("""
This page provides a high-level overview of the business performance,
highlighting the most important KPIs, best-performing entities,
business insights, and strategic recommendations.
""")

# ===============================
# KPI CARDS
# ===============================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "💰 Revenue",
    f"${kpi['sales']:,.0f}"
)

c2.metric(
    "📈 Profit",
    f"${kpi['profit']:,.0f}"
)

c3.metric(
    "📊 Margin",
    f"{kpi['margin']:.2f}%"
)

c4.metric(
    "👥 Customers",
    kpi["customers"]
)

c5.metric(
    "🎯 Avg Discount",
    f"{kpi['discount']:.2f}%"
)

st.divider()

# ===============================
# BUSINESS PERFORMANCE
# ===============================

market_profit = (
    df.groupby("Market")["Order Profit Per Order"]
      .sum()
      .sort_values(ascending=False)
)

category_profit = (
    df.groupby("Category Name")["Order Profit Per Order"]
      .sum()
      .sort_values(ascending=False)
)

customer_profit = (
    df.groupby("Customer Id")["Order Profit Per Order"]
      .sum()
      .sort_values(ascending=False)
)

product_profit = (
    df.groupby("Product Name")["Order Profit Per Order"]
      .sum()
      .sort_values(ascending=False)
)

best_market = market_profit.index[0]
worst_market = market_profit.index[-1]

best_category = category_profit.index[0]
worst_category = category_profit.index[-1]

best_customer = customer_profit.index[0]
worst_customer = customer_profit.index[-1]

best_product = product_profit.index[0]
worst_product = product_profit.index[-1]

# ===============================
# BEST & WORST PERFORMANCE
# ===============================

st.header("🏆 Business Performance Summary")

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
### 🌍 Best Market

**{best_market}**

Profit

**${market_profit.iloc[0]:,.0f}**
""")

    st.success(f"""
### 📦 Best Category

**{best_category}**

Profit

**${category_profit.iloc[0]:,.0f}**
""")

    st.success(f"""
### 👤 Best Customer

Customer ID

**{best_customer}**

Profit

**${customer_profit.iloc[0]:,.0f}**
""")

    st.success(f"""
### 📈 Best Product

**{best_product}**

Profit

**${product_profit.iloc[0]:,.0f}**
""")

with col2:

    st.error(f"""
### 📉 Weakest Market

**{worst_market}**

Profit

**${market_profit.iloc[-1]:,.0f}**
""")

    st.error(f"""
### 📦 Weakest Category

**{worst_category}**

Profit

**${category_profit.iloc[-1]:,.0f}**
""")

    st.error(f"""
### 👤 Lowest Customer

Customer ID

**{worst_customer}**

Profit

**${customer_profit.iloc[-1]:,.0f}**
""")

    st.error(f"""
### 📉 Lowest Product

**{worst_product}**

Profit

**${product_profit.iloc[-1]:,.0f}**
""")

st.divider()

# ===============================
# EXECUTIVE VISUALS
# ===============================

left, right = st.columns(2)

with left:

    st.subheader("🌍 Profit by Market")

    market_df = (
        df.groupby("Market")["Order Profit Per Order"]
          .sum()
          .reset_index()
    )

    fig = px.bar(
        market_df,
        x="Market",
        y="Order Profit Per Order",
        color="Order Profit Per Order",
        title="Market Profitability"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("📦 Profit by Category")

    category_df = (
        df.groupby("Category Name")["Order Profit Per Order"]
          .sum()
          .reset_index()
    )

    fig = px.bar(
        category_df,
        x="Category Name",
        y="Order Profit Per Order",
        color="Order Profit Per Order",
        title="Category Profitability"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===============================
# TOP 10 PRODUCTS
# ===============================

st.subheader("🏆 Top 10 Profitable Products")

top_products = (
    df.groupby("Product Name")["Order Profit Per Order"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    top_products,
    x="Order Profit Per Order",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================
# EXECUTIVE INSIGHTS
# =====================================

st.header("📌 Executive Insights")

st.info(f"""

### Key Business Findings

✅ Total Revenue Generated: **${kpi['sales']:,.0f}**

✅ Total Profit Earned: **${kpi['profit']:,.0f}**

✅ Overall Profit Margin: **{kpi['margin']:.2f}%**

✅ Best Performing Market: **{best_market}**

✅ Best Product Category: **{best_category}**

✅ Highest Profit Product: **{best_product}**

✅ Total Customers Served: **{kpi['customers']:,}**

""")

st.divider()

# =====================================
# STRATEGIC RECOMMENDATIONS
# =====================================

st.header("💡 Strategic Recommendations")

col1, col2 = st.columns(2)

with col1:

    st.success("""
### Revenue Growth

• Increase investment in high-profit markets.

• Promote best-selling profitable products.

• Strengthen relationships with top-value customers.

• Expand high-performing product categories.
""")

with col2:

    st.warning("""
### Profit Optimization

• Reduce excessive discounts.

• Review loss-making products.

• Improve pricing strategy.

• Optimize logistics for low-margin regions.
""")

st.divider()

# =====================================
# EXECUTIVE SUMMARY TABLE
# =====================================

st.header("📋 Executive Summary")

summary = {
    "Metric": [
        "Total Revenue",
        "Total Profit",
        "Profit Margin",
        "Customers",
        "Best Market",
        "Worst Market",
        "Best Category",
        "Worst Category",
        "Best Product",
        "Worst Product"
    ],

    "Value": [
        f"${kpi['sales']:,.0f}",
        f"${kpi['profit']:,.0f}",
        f"{kpi['margin']:.2f}%",
        kpi["customers"],
        best_market,
        worst_market,
        best_category,
        worst_category,
        best_product,
        worst_product
    ]
}

import pandas as pd

summary_df = pd.DataFrame(summary)

st.dataframe(
    summary_df,
    use_container_width=True
)

st.divider()

# =====================================
# DOWNLOAD REPORT
# =====================================

csv = summary_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Executive Summary",
    csv,
    "Executive_Summary.csv",
    "text/csv"
)

st.divider()

# =====================================
# PROJECT CONCLUSION
# =====================================

st.header("🎯 Project Conclusion")

st.success("""

This dashboard successfully transforms operational supply chain data into actionable business intelligence.

It enables management to:

✔ Identify profitable customers.

✔ Discover high-performing products.

✔ Measure the impact of discounts.

✔ Compare market performance.

✔ Improve pricing decisions.

✔ Support strategic business planning.

The project demonstrates how data analytics can shift decision-making from
**revenue-focused** to **profit-focused**, helping APL Logistics improve long-term commercial performance.

""")

st.markdown("---")

st.caption("Developed by Rohin Sabarwal | B.Tech CSE | Unified Mentor Internship | 2026")