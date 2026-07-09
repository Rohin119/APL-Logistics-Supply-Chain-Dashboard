import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, calculate_kpis

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👥",
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
st.title("👥 Customer Analysis Dashboard")

# --------------------------------------------------
# Customer Summary
# --------------------------------------------------
customer = (
    filtered_df.groupby(
        ["Customer Id", "Customer Fname", "Customer Lname"]
    )
    .agg({
        "Sales": "sum",
        "Order Profit Per Order": "sum",
        "Order Item Discount": "sum",
        "Order Item Quantity": "sum"
    })
    .reset_index()
)

customer["Customer Name"] = (
    customer["Customer Fname"] + " " +
    customer["Customer Lname"]
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
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
    "📊 Profit Margin",
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

# --------------------------------------------------
# Top Customers
# --------------------------------------------------
st.subheader("🏆 Top 10 Customers by Profit")

top = customer.nlargest(10, "Order Profit Per Order")

fig = px.bar(
    top,
    x="Order Profit Per Order",
    y="Customer Name",
    orientation="h",
    color="Order Profit Per Order",
    title="Top 10 Customers by Profit"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Bottom Customers
# --------------------------------------------------
st.subheader("📉 Bottom 10 Customers by Profit")

bottom = customer.nsmallest(10, "Order Profit Per Order")

fig = px.bar(
    bottom,
    x="Order Profit Per Order",
    y="Customer Name",
    orientation="h",
    color="Order Profit Per Order",
    title="Bottom 10 Customers by Profit"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Sales vs Profit
# --------------------------------------------------
st.subheader("📊 Sales vs Profit")

fig = px.scatter(
    customer,
    x="Sales",
    y="Order Profit Per Order",
    size="Order Item Quantity",
    color="Order Item Discount",
    hover_name="Customer Name",
    title="Sales vs Profit"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Top Discount Customers
# --------------------------------------------------
st.subheader("🎯 Top Discount Customers")

discount = customer.nlargest(
    10,
    "Order Item Discount"
)

fig = px.bar(
    discount,
    x="Order Item Discount",
    y="Customer Name",
    orientation="h",
    color="Order Item Discount",
    title="Top Discount Customers"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Profit Distribution
# --------------------------------------------------
st.subheader("📈 Customer Profit Distribution")

fig = px.histogram(
    customer,
    x="Order Profit Per Order",
    nbins=40,
    title="Customer Profit Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Customer Table
# --------------------------------------------------
st.subheader("📋 Customer Details")

st.dataframe(customer, use_container_width=True)

# --------------------------------------------------
# Download Report
# --------------------------------------------------
csv = customer.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Customer Report",
    data=csv,
    file_name="Customer_Report.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Business Insights
# --------------------------------------------------
st.markdown("---")

st.info("""
### 💡 Business Insights

- Top customers contribute a significant share of total profit.
- Some customers generate high sales but relatively low profit, indicating margin pressure.
- Customers receiving the largest discounts should be reviewed to ensure they remain profitable.
- Customer retention efforts should prioritize the highest-profit customers.
""")