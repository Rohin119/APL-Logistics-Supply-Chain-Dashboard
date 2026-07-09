import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, calculate_kpis

# --------------------------------------------------
# PAGE CONFIG (Must be first Streamlit command)
# --------------------------------------------------
st.set_page_config(
    page_title="APL Logistics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = load_data()
kpi = calculate_kpis(df)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.image("assets/logo.png", width=170)

st.sidebar.markdown("## 📦 APL Logistics")

st.sidebar.markdown("""
Supply Chain Intelligence Dashboard

---

### 📑 Dashboard Pages

🏠 Home

💰 Revenue & Profit

👥 Customer Analysis

📦 Product Analysis

🎯 Discount Analysis

🌍 Market Analysis

📊 Executive Summary

ℹ About Project
""")

st.sidebar.success("Unified Mentor Internship Project")

# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero">

<h1>📦 APL Logistics Dashboard</h1>

<h3>Customer • Product • Profitability • Supply Chain Intelligence</h3>

<p>

Turn raw operational data into strategic business decisions.

Analyze revenue, profitability, customer value, products,
discount impact and global market performance — all in one dashboard.

</p>

<span class="badge">💰 Revenue</span>

<span class="badge">📈 Profit</span>

<span class="badge">👥 Customers</span>

<span class="badge">📦 Products</span>

<span class="badge">🎯 Discounts</span>

<span class="badge">🌍 Markets</span>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# EXECUTIVE OVERVIEW
# ==========================================================

left, right = st.columns([2.2,1])

with left:

    st.info("""
## 🚀 Executive Overview

This Business Intelligence Dashboard helps management answer critical questions:

✔ Which customers generate the highest profit?

✔ Which products are truly profitable?

✔ How much profit is lost due to discounts?

✔ Which markets deserve future investment?

✔ Which categories reduce profitability?

Use the navigation panel to explore each analytical module.
""")

with right:

    st.metric("📦 Orders", f"{len(df):,}")

    st.metric("👥 Customers", df["Customer Id"].nunique())

    st.metric("📦 Products", df["Product Name"].nunique())

    st.metric("🌍 Markets", df["Market"].nunique())

st.divider()

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📊 Key Performance Indicators")

c1,c2,c3,c4,c5 = st.columns(5)

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

# ==========================================================
# QUICK OVERVIEW
# ==========================================================

st.header("📈 Business Performance Overview")

left, right = st.columns(2)

# ----------------------------------------------------------
# Revenue by Market
# ----------------------------------------------------------

with left:

    market = (
        df.groupby("Market")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        market,
        x="Market",
        y="Sales",
        color="Sales",
        title="Revenue by Market",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Market",
        yaxis_title="Revenue",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Revenue by Category
# ----------------------------------------------------------

with right:

    category = (
        df.groupby("Category Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.pie(
        category,
        names="Category Name",
        values="Sales",
        hole=0.55,
        title="Top Categories by Revenue"
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================================================
# DASHBOARD MODULES
# ==========================================================

st.header("🚀 Dashboard Modules")

c1, c2, c3 = st.columns(3)

with c1:

    st.success("""
### 💰 Revenue & Profit

✔ Revenue KPIs

✔ Profit KPIs

✔ Margin Analysis

✔ Revenue Distribution
""")

with c2:

    st.success("""
### 👥 Customer Analysis

✔ Top Customers

✔ Customer Value

✔ Customer Segments

✔ Profit Contribution
""")

with c3:

    st.success("""
### 📦 Product Analysis

✔ Top Products

✔ Loss Products

✔ Category Margin

✔ Product Performance
""")

c4, c5, c6 = st.columns(3)

with c4:

    st.success("""
### 🎯 Discount Analysis

✔ Discount Impact

✔ Margin Erosion

✔ Profit Ratio

✔ What-if Analysis
""")

with c5:

    st.success("""
### 🌍 Market Analysis

✔ Revenue by Market

✔ Profit by Region

✔ World Map

✔ Country Analysis
""")

with c6:

    st.success("""
### 📊 Executive Summary

✔ Business Insights

✔ Recommendations

✔ Key Findings

✔ Decision Support
""")

st.divider()

# ==========================================================
# BUSINESS OBJECTIVE
# ==========================================================

left, right = st.columns([2,1])

with left:

    st.subheader("🎯 Business Objective")

    st.info("""
This dashboard transforms operational supply chain data into
commercial intelligence.

It helps identify:

• High-value customers

• High-profit products

• Loss-making categories

• Discount-driven margin erosion

• Profitable markets

• Revenue vs Profit performance

The ultimate goal is to support data-driven business decisions.
""")

with right:

    st.subheader("📦 Dataset Overview")

    st.metric("Orders", f"{len(df):,}")
    st.metric("Products", df["Product Name"].nunique())
    st.metric("Customers", df["Customer Id"].nunique())
    st.metric("Markets", df["Market"].nunique())
    st.metric("Categories", df["Category Name"].nunique())

st.divider()

# ==========================================================
# QUICK BUSINESS INSIGHTS
# ==========================================================

st.header("📊 Executive Insights")

market_profit = (
    df.groupby("Market")["Order Profit Per Order"]
      .sum()
      .sort_values(ascending=False)
)

category_sales = (
    df.groupby("Category Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

customer_profit = (
    df.groupby("Customer Id")["Order Profit Per Order"]
      .sum()
      .sort_values(ascending=False)
)

col1, col2, col3 = st.columns(3)

with col1:
    st.success(f"""
### 🌍 Best Market

**{market_profit.index[0]}**

💰 Profit

### **${market_profit.iloc[0]:,.0f}**
""")

with col2:
    st.success(f"""
### 📦 Best Category

**{category_sales.index[0]}**

💰 Revenue

### **${category_sales.iloc[0]:,.0f}**
""")

with col3:
    st.success(f"""
### 👤 Top Customer

Customer ID

**{customer_profit.index[0]}**

💰 Profit

### **${customer_profit.iloc[0]:,.0f}**
""")

st.divider()

# ==========================================================
# WHY THIS DASHBOARD?
# ==========================================================

st.header("💡 Why This Dashboard?")

left, right = st.columns([2, 1])

# ---------------- Left Column ----------------

with left:

    st.markdown("""
### 📈 Business Benefits

This dashboard enables **APL Logistics** to:

✅ Identify high-value customers

✅ Compare revenue with actual profitability

✅ Detect discount-driven margin erosion

✅ Discover profitable products and categories

✅ Compare markets and regions

✅ Improve pricing strategies

✅ Support executive decision making

Instead of focusing only on **Sales**, management can now make
**Profit-driven Business Decisions**.
""")

# ---------------- Right Column ----------------

with right:

    summary = pd.DataFrame({
        "Metric": [
            "Revenue",
            "Profit",
            "Customers"
        ],
        "Value": [
            kpi["sales"],
            kpi["profit"],
            kpi["customers"]
        ]
    })

    fig = px.pie(
        summary,
        names="Metric",
        values="Value",
        hole=0.65,
        title="Executive KPI Distribution",
        color="Metric"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        height=380,
        showlegend=False,
        margin=dict(l=10, r=10, t=60, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================================================
# TECHNOLOGY STACK
# ==========================================================

st.header("🛠 Technology Stack")

tech1, tech2, tech3, tech4 = st.columns(4)

tech1.info("""
### 🐍 Python

Backend Logic
""")

tech2.info("""
### 📊 Pandas

Data Analysis
""")

tech3.info("""
### 📈 Plotly

Interactive Charts
""")

tech4.info("""
### 🌐 Streamlit

Dashboard Framework
""")

st.divider()

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.header("📚 Project Information")

st.markdown("""
### Project Title

**Customer, Product, and Profitability Performance Analysis in Supply Chain Operations**

### Organization

APL Logistics (KWE Group)

### Objective

To transform operational supply chain data into commercial intelligence
that helps optimize profitability, customer value, discount strategy,
product performance, and market expansion.
""")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
"""
---
<div style="text-align:center;">

# 📦 APL Logistics Dashboard

### Developed by Rohin Sabarwal

**B.Tech Computer Science Engineering**

**BML Munjal University**

Unified Mentor Internship Project • 2026

Made with ❤️ using Python, Pandas, Plotly & Streamlit

</div>
""",
unsafe_allow_html=True
)