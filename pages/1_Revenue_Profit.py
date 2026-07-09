import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, calculate_kpis

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Revenue & Profit Analysis",
    page_icon="💰",
    layout="wide"
)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------
df = load_data()
filtered_df = apply_filters(df)
kpi = calculate_kpis(filtered_df)

# ----------------------------------------------------
# Page Title
# ----------------------------------------------------
st.title("💰 Revenue & Profit Analysis")

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Revenue", f"${kpi['sales']:,.0f}")
c2.metric("📈 Profit", f"${kpi['profit']:,.0f}")
c3.metric("📊 Profit Margin", f"{kpi['margin']:.2f}%")
c4.metric("👥 Customers", kpi["customers"])
c5.metric("🎯 Avg Discount", f"{kpi['discount']:.2f}%")

st.divider()

# ----------------------------------------------------
# Revenue vs Profit
# ----------------------------------------------------
st.subheader("📊 Revenue vs Profit")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Order Profit Per Order",
    color="Market",
    size="Order Item Quantity",
    hover_name="Product Name",
    title="Revenue vs Profit by Product"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Sales Distribution
# ----------------------------------------------------
st.subheader("📈 Sales Distribution")

fig = px.histogram(
    filtered_df,
    x="Sales",
    nbins=40,
    title="Distribution of Sales"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Profit Distribution
# ----------------------------------------------------
st.subheader("📉 Profit Distribution")

fig = px.histogram(
    filtered_df,
    x="Order Profit Per Order",
    nbins=40,
    title="Distribution of Profit"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Revenue by Market
# ----------------------------------------------------
st.subheader("🌍 Revenue by Market")

market_sales = (
    filtered_df.groupby("Market")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    market_sales,
    x="Market",
    y="Sales",
    color="Sales",
    title="Revenue by Market"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Profit by Market
# ----------------------------------------------------
st.subheader("💵 Profit by Market")

market_profit = (
    filtered_df.groupby("Market")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    market_profit,
    x="Market",
    y="Order Profit Per Order",
    color="Order Profit Per Order",
    title="Profit by Market"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Top 10 Profitable Products
# ----------------------------------------------------
st.subheader("🏆 Top 10 Profitable Products")

top_products = (
    filtered_df.groupby("Product Name")["Order Profit Per Order"]
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

# ----------------------------------------------------
# Bottom 10 Products
# ----------------------------------------------------
st.subheader("📉 Bottom 10 Products")

bottom_products = (
    filtered_df.groupby("Product Name")["Order Profit Per Order"]
    .sum()
    .sort_values()
    .head(10)
    .reset_index()
)

fig = px.bar(
    bottom_products,
    x="Order Profit Per Order",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Revenue by Category
# ----------------------------------------------------
st.subheader("📦 Revenue by Category")

category_sales = (
    filtered_df.groupby("Category Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="Category Name",
    y="Sales",
    color="Sales"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Business Insights
# ----------------------------------------------------
st.subheader("💡 Business Insights")

st.info("""
• Markets generating high revenue are not always the most profitable.

• Focus on products with high profit margins instead of only high sales.

• Review low-performing products to improve profitability.

• Optimize pricing and discount strategies for products with high revenue but low profit.
""")

# ----------------------------------------------------
# Data Table
# ----------------------------------------------------
st.subheader("📋 Filtered Dataset")

st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# Download Button
# ----------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="Revenue_Profit_Report.csv",
    mime="text/csv"
)