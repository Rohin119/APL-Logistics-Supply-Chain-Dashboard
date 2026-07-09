import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, calculate_kpis

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Revenue & Profit Analysis",
    page_icon="💰",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()
filtered_df = apply_filters(df)
kpi = calculate_kpis(filtered_df)

# ==========================================================
# CACHE CSV
# ==========================================================

@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# ==========================================================
# SAMPLE DATA FOR SCATTER
# (Huge speed improvement)
# ==========================================================

scatter_df = filtered_df.sample(
    min(5000, len(filtered_df)),
    random_state=42
)

# ==========================================================
# TITLE
# ==========================================================

st.title("💰 Revenue & Profit Analysis")

# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Revenue", f"${kpi['sales']:,.0f}")
c2.metric("📈 Profit", f"${kpi['profit']:,.0f}")
c3.metric("📊 Profit Margin", f"{kpi['margin']:.2f}%")
c4.metric("👥 Customers", kpi["customers"])
c5.metric("🎯 Avg Discount", f"{kpi['discount']:.2f}%")

st.divider()

# ==========================================================
# REVENUE VS PROFIT
# ==========================================================

st.subheader("📊 Revenue vs Profit")

fig = px.scatter(
    scatter_df,
    x="Sales",
    y="Order Profit Per Order",
    color="Market",
    size="Order Item Quantity",
    hover_name="Product Name",
    title="Revenue vs Profit by Product"
)

fig.update_layout(height=550)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# SALES DISTRIBUTION
# ==========================================================

st.subheader("📈 Sales Distribution")

fig = px.histogram(
    filtered_df,
    x="Sales",
    nbins=40,
    title="Distribution of Sales"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# PROFIT DISTRIBUTION
# ==========================================================

st.subheader("📉 Profit Distribution")

fig = px.histogram(
    filtered_df,
    x="Order Profit Per Order",
    nbins=40,
    title="Distribution of Profit"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)
# ==========================================================
# REVENUE BY MARKET
# ==========================================================

st.subheader("🌍 Revenue by Market")

market_sales = (
    filtered_df.groupby("Market", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

fig = px.bar(
    market_sales,
    x="Market",
    y="Sales",
    color="Sales",
    title="Revenue by Market"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# PROFIT BY MARKET
# ==========================================================

st.subheader("💵 Profit by Market")

market_profit = (
    filtered_df.groupby("Market", as_index=False)["Order Profit Per Order"]
    .sum()
    .sort_values("Order Profit Per Order", ascending=False)
)

fig = px.bar(
    market_profit,
    x="Market",
    y="Order Profit Per Order",
    color="Order Profit Per Order",
    title="Profit by Market"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# TOP 10 PRODUCTS
# ==========================================================

st.subheader("🏆 Top 10 Profitable Products")

top_products = (
    filtered_df.groupby("Product Name", as_index=False)["Order Profit Per Order"]
    .sum()
    .nlargest(10, "Order Profit Per Order")
)

fig = px.bar(
    top_products,
    x="Order Profit Per Order",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order"
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# BOTTOM 10 PRODUCTS
# ==========================================================

st.subheader("📉 Bottom 10 Products")

bottom_products = (
    filtered_df.groupby("Product Name", as_index=False)["Order Profit Per Order"]
    .sum()
    .nsmallest(10, "Order Profit Per Order")
)

fig = px.bar(
    bottom_products,
    x="Order Profit Per Order",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order"
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# REVENUE BY CATEGORY
# ==========================================================

st.subheader("📦 Revenue by Category")

category_sales = (
    filtered_df.groupby("Category Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

fig = px.bar(
    category_sales,
    x="Category Name",
    y="Sales",
    color="Sales"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.subheader("💡 Business Insights")

st.info("""
• Markets generating high revenue are not always the most profitable.

• Focus on products with high profit margins instead of only high sales.

• Review low-performing products to improve profitability.

• Optimize pricing and discount strategies for products with high revenue but low profit.
""")

# ==========================================================
# DATA PREVIEW
# ==========================================================

st.subheader("📋 Filtered Dataset")

st.caption(f"Showing first 100 rows out of {len(filtered_df):,} filtered records.")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True,
    height=450
)

# ==========================================================
# DOWNLOAD
# ==========================================================

csv = convert_csv(filtered_df)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="Revenue_Profit_Report.csv",
    mime="text/csv"
)