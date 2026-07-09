import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, apply_filters, calculate_kpis

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Discount Analysis",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = load_data()
filtered_df = apply_filters(df)
kpi = calculate_kpis(filtered_df)

st.title("🎯 Discount Impact Analysis")

# --------------------------------------------------
# Discount Slider
# --------------------------------------------------
st.sidebar.subheader("🎯 Discount Analysis")

discount_range = st.sidebar.slider(
    "Discount Rate",
    float(filtered_df["Order Item Discount Rate"].min()),
    float(filtered_df["Order Item Discount Rate"].max()),
    (
        float(filtered_df["Order Item Discount Rate"].min()),
        float(filtered_df["Order Item Discount Rate"].max())
    )
)

filtered_df = filtered_df[
    (filtered_df["Order Item Discount Rate"] >= discount_range[0]) &
    (filtered_df["Order Item Discount Rate"] <= discount_range[1])
]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
discount_impact = (
    filtered_df["Order Item Discount"].sum() /
    filtered_df["Sales"].sum()
) * 100 if filtered_df["Sales"].sum() != 0 else 0

avg_profit_ratio = filtered_df["Order Item Profit Ratio"].mean()

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
    "🎯 Discount Impact",
    f"{discount_impact:.2f}%"
)

c5.metric(
    "📉 Avg Profit Ratio",
    f"{avg_profit_ratio:.2f}"
)

st.divider()

# --------------------------------------------------
# Discount Rate vs Profit Ratio
# --------------------------------------------------
st.subheader("📊 Discount Rate vs Profit Ratio")

fig = px.scatter(
    filtered_df,
    x="Order Item Discount Rate",
    y="Order Item Profit Ratio",
    color="Market",
    hover_name="Product Name",
    title="Discount Rate vs Profit Ratio"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Discount Distribution
# --------------------------------------------------
st.subheader("📈 Discount Distribution")

fig = px.histogram(
    filtered_df,
    x="Order Item Discount Rate",
    nbins=30,
    title="Discount Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Discount Categories
# --------------------------------------------------
filtered_df["Discount Category"] = pd.cut(
    filtered_df["Order Item Discount Rate"],
    bins=[0, 0.1, 0.2, 0.3, 0.4, 1],
    labels=[
        "0-10%",
        "10-20%",
        "20-30%",
        "30-40%",
        "40%+"
    ]
)

margin = (
    filtered_df.groupby("Discount Category")
    .agg({
        "Order Profit Per Order":"mean"
    })
    .reset_index()
)

st.subheader("📉 Average Profit by Discount Category")

fig = px.bar(
    margin,
    x="Discount Category",
    y="Order Profit Per Order",
    color="Order Profit Per Order"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Correlation Heatmap
# --------------------------------------------------
st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[
    [
        "Order Item Discount Rate",
        "Order Item Discount",
        "Order Profit Per Order",
        "Order Item Profit Ratio",
        "Sales"
    ]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu",
    title="Correlation Matrix"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Margin Erosion Analysis
# --------------------------------------------------
st.subheader("📉 Margin Erosion Analysis")

erosion = (
    filtered_df.groupby("Discount Category")
    .agg({
        "Sales": "sum",
        "Order Profit Per Order": "sum"
    })
    .reset_index()
)

erosion["Profit Margin (%)"] = (
    erosion["Order Profit Per Order"] /
    erosion["Sales"] * 100
).round(2)

fig = px.line(
    erosion,
    x="Discount Category",
    y="Profit Margin (%)",
    markers=True,
    title="Profit Margin by Discount Category"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# What-if Discount Simulator
# --------------------------------------------------
st.subheader("🧮 What-if Discount Simulator")

sim_discount = st.slider(
    "Assume Average Discount (%)",
    0,
    50,
    20
)

estimated_profit = (
    filtered_df["Sales"].sum() *
    (1 - sim_discount / 100) *
    filtered_df["Order Item Profit Ratio"].mean()
)

st.metric(
    "Estimated Profit",
    f"${estimated_profit:,.0f}"
)

# --------------------------------------------------
# Top Discounted Products
# --------------------------------------------------
st.subheader("🏷️ Top 10 Discounted Products")

top_discount = (
    filtered_df.groupby("Product Name")
    .agg({
        "Order Item Discount": "sum",
        "Order Profit Per Order": "sum"
    })
    .reset_index()
)

top_discount = top_discount.nlargest(
    10,
    "Order Item Discount"
)

fig = px.bar(
    top_discount,
    x="Order Item Discount",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order",
    title="Top Discounted Products"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Orders Table
# --------------------------------------------------
st.subheader("📋 Discount Analysis Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# --------------------------------------------------
# Download Button
# --------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Discount Report",
    data=csv,
    file_name="Discount_Report.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Business Insights
# --------------------------------------------------
st.subheader("💡 Business Insights")

st.info("""
• Higher discount rates generally reduce overall profit margins.

• Discounts above 30% should be carefully evaluated because they often lead to significant margin erosion.

• Products receiving large discounts but generating low profit should be reviewed.

• Optimize discount strategies to balance customer acquisition with profitability.

• The What-if Simulator helps estimate how changing discount levels could impact profits.
""")