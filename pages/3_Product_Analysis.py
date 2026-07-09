import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, calculate_kpis

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = load_data()
filtered_df = apply_filters(df)
kpi = calculate_kpis(filtered_df)

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.title("📦 Product & Category Analysis")

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Revenue", f"${kpi['sales']:,.0f}")
c2.metric("📈 Profit", f"${kpi['profit']:,.0f}")
c3.metric("📊 Profit Margin", f"{kpi['margin']:.2f}%")
c4.metric("👥 Customers", kpi["customers"])
c5.metric("🎯 Avg Discount", f"{kpi['discount']:.2f}%")

st.divider()

# --------------------------------------------------
# Product Summary
# --------------------------------------------------
product = (
    filtered_df.groupby("Product Name")
    .agg({
        "Sales": "sum",
        "Order Profit Per Order": "sum",
        "Order Item Discount": "sum",
        "Order Item Quantity": "sum"
    })
    .reset_index()
)

product["Profit Margin (%)"] = (
    product["Order Profit Per Order"] /
    product["Sales"] * 100
).round(2)

# --------------------------------------------------
# Top 10 Products
# --------------------------------------------------
st.subheader("🏆 Top 10 Products by Profit")

top = product.nlargest(10, "Order Profit Per Order")

fig = px.bar(
    top,
    x="Order Profit Per Order",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order",
    title="Top 10 Products by Profit"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Bottom 10 Products
# --------------------------------------------------
st.subheader("📉 Bottom 10 Products")

bottom = product.nsmallest(10, "Order Profit Per Order")

fig = px.bar(
    bottom,
    x="Order Profit Per Order",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order",
    title="Bottom 10 Products"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Most Sold Products
# --------------------------------------------------
st.subheader("📦 Most Sold Products")

sold = product.nlargest(10, "Order Item Quantity")

fig = px.bar(
    sold,
    x="Order Item Quantity",
    y="Product Name",
    orientation="h",
    color="Order Item Quantity",
    title="Most Sold Products"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Sales vs Profit
# --------------------------------------------------
st.subheader("📊 Sales vs Profit")

fig = px.scatter(
    product,
    x="Sales",
    y="Order Profit Per Order",
    size="Order Item Quantity",
    color="Profit Margin (%)",
    hover_name="Product Name",
    title="Sales vs Profit"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Category Summary
# --------------------------------------------------
category_profit = (
    filtered_df.groupby("Category Name")
    .agg({
        "Sales": "sum",
        "Order Profit Per Order": "sum"
    })
    .reset_index()
)

category_profit["Profit Margin (%)"] = (
    category_profit["Order Profit Per Order"] /
    category_profit["Sales"] * 100
).round(2)

# --------------------------------------------------
# Category Profit Margin
# --------------------------------------------------
st.subheader("📈 Category Profit Margin")

fig = px.bar(
    category_profit,
    x="Category Name",
    y="Profit Margin (%)",
    color="Profit Margin (%)",
    title="Category Profit Margin"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Category Profitability Heatmap
# --------------------------------------------------
st.subheader("🔥 Category Profitability Heatmap")

heatmap = filtered_df.pivot_table(
    index="Category Name",
    columns="Market",
    values="Order Profit Per Order",
    aggfunc="sum",
    fill_value=0
)

fig = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    title="Category vs Market Profit"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Treemap
# --------------------------------------------------
st.subheader("🌳 Sales by Category")

fig = px.treemap(
    category_profit,
    path=["Category Name"],
    values="Sales",
    color="Order Profit Per Order",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Profit Margin Distribution
# --------------------------------------------------
st.subheader("📉 Product Profit Margin Distribution")

fig = px.histogram(
    product,
    x="Profit Margin (%)",
    nbins=40,
    title="Profit Margin Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# High Revenue - Low Margin Products
# --------------------------------------------------
st.subheader("⚠️ High Revenue but Low Margin Products")

high_revenue_low_margin = product[
    (product["Sales"] > product["Sales"].median()) &
    (product["Profit Margin (%)"] < product["Profit Margin (%)"].median())
].sort_values(
    by="Sales",
    ascending=False
)

st.dataframe(
    high_revenue_low_margin,
    use_container_width=True
)

# --------------------------------------------------
# Top Loss Making Products
# --------------------------------------------------
st.subheader("❌ Loss Making Products")

loss_products = product[
    product["Order Profit Per Order"] < 0
].sort_values(
    by="Order Profit Per Order"
)

st.dataframe(
    loss_products,
    use_container_width=True
)

# --------------------------------------------------
# Product Details
# --------------------------------------------------
st.subheader("📋 Product Details")

st.dataframe(
    product,
    use_container_width=True
)

# --------------------------------------------------
# Download Button
# --------------------------------------------------
csv = product.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Product Report",
    data=csv,
    file_name="Product_Report.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Business Insights
# --------------------------------------------------
st.subheader("💡 Business Insights")

st.info("""
• Products with high sales do not always generate high profits.

• Categories with low profit margins should be reviewed for pricing and discount strategies.

• Focus on high-margin products to maximize profitability.

• High-revenue but low-margin products may require pricing optimization.

• Loss-making products should be analyzed to determine whether they should be repriced or discontinued.
""")