import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, apply_filters, calculate_kpis

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Discount Analysis",
    page_icon="🎯",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()
filtered_df = apply_filters(df)
kpi = calculate_kpis(filtered_df)

st.title("🎯 Discount Impact Analysis")

# ==========================================================
# CACHE CSV
# ==========================================================

@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# ==========================================================
# CACHE CORRELATION
# ==========================================================

@st.cache_data
def correlation_matrix(df):

    return df[
        [
            "Order Item Discount Rate",
            "Order Item Discount",
            "Order Profit Per Order",
            "Order Item Profit Ratio",
            "Sales"
        ]
    ].corr()

# ==========================================================
# CACHE TOP PRODUCTS
# ==========================================================

@st.cache_data
def top_discount_products(df):

    return (
        df.groupby("Product Name", as_index=False)
        .agg({
            "Order Item Discount":"sum",
            "Order Profit Per Order":"sum"
        })
        .nlargest(10,"Order Item Discount")
    )

# ==========================================================
# SIDEBAR
# ==========================================================

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

filtered_df = filtered_df.copy()

# ==========================================================
# SAMPLE FOR SCATTER PLOT
# ==========================================================

scatter_df = filtered_df.sample(
    min(5000, len(filtered_df)),
    random_state=42
)
# ==========================================================
# KPIs
# ==========================================================

discount_impact = (
    filtered_df["Order Item Discount"].sum() /
    filtered_df["Sales"].sum() * 100
) if filtered_df["Sales"].sum() != 0 else 0

avg_profit_ratio = filtered_df["Order Item Profit Ratio"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Revenue", f"${kpi['sales']:,.0f}")
c2.metric("📈 Profit", f"${kpi['profit']:,.0f}")
c3.metric("📊 Margin", f"{kpi['margin']:.2f}%")
c4.metric("🎯 Discount Impact", f"{discount_impact:.2f}%")
c5.metric("📉 Avg Profit Ratio", f"{avg_profit_ratio:.2f}")

st.divider()

# ==========================================================
# DISCOUNT RATE VS PROFIT RATIO
# ==========================================================

st.subheader("📊 Discount Rate vs Profit Ratio")

fig = px.scatter(
    scatter_df,
    x="Order Item Discount Rate",
    y="Order Item Profit Ratio",
    color="Market",
    hover_name="Product Name",
    title="Discount Rate vs Profit Ratio"
)

fig.update_layout(height=550)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# DISCOUNT DISTRIBUTION
# ==========================================================

st.subheader("📈 Discount Distribution")

fig = px.histogram(
    filtered_df,
    x="Order Item Discount Rate",
    nbins=30,
    title="Discount Distribution"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# DISCOUNT CATEGORY
# ==========================================================

filtered_df["Discount Category"] = pd.cut(
    filtered_df["Order Item Discount Rate"],
    bins=[0,0.1,0.2,0.3,0.4,1],
    labels=[
        "0-10%",
        "10-20%",
        "20-30%",
        "30-40%",
        "40%+"
    ]
)

margin = (
    filtered_df.groupby(
        "Discount Category",
        as_index=False
    )["Order Profit Per Order"]
    .mean()
)

st.subheader("📉 Average Profit by Discount Category")

fig = px.bar(
    margin,
    x="Discount Category",
    y="Order Profit Per Order",
    color="Order Profit Per Order"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

st.subheader("🔥 Correlation Heatmap")

corr = correlation_matrix(filtered_df)

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu",
    title="Correlation Matrix"
)

fig.update_layout(height=600)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# MARGIN EROSION
# ==========================================================

st.subheader("📉 Margin Erosion Analysis")

erosion = (
    filtered_df.groupby(
        "Discount Category",
        as_index=False
    )
    .agg({
        "Sales":"sum",
        "Order Profit Per Order":"sum"
    })
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

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# WHAT-IF SIMULATOR
# ==========================================================

st.subheader("🧮 What-if Discount Simulator")

sim_discount = st.slider(
    "Assume Average Discount (%)",
    0,
    50,
    20
)

estimated_profit = (
    filtered_df["Sales"].sum()
    * (1 - sim_discount / 100)
    * filtered_df["Order Item Profit Ratio"].mean()
)

st.metric(
    "Estimated Profit",
    f"${estimated_profit:,.0f}"
)

st.divider()
# ==========================================================
# TOP DISCOUNTED PRODUCTS
# ==========================================================

st.subheader("🏷️ Top 10 Discounted Products")

top_discount = top_discount_products(filtered_df)

fig = px.bar(
    top_discount,
    x="Order Item Discount",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order",
    title="Top Discounted Products"
)

fig.update_layout(height=550)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ==========================================================
# SUMMARY TABLE
# ==========================================================

st.subheader("📊 Discount Summary")

summary = (
    filtered_df.groupby("Discount Category", as_index=False)
    .agg({
        "Sales":"sum",
        "Order Profit Per Order":"sum",
        "Order Item Discount":"sum",
        "Order Item Quantity":"sum"
    })
)

st.dataframe(
    summary,
    use_container_width=True,
    height=250
)

# ==========================================================
# DATA PREVIEW
# ==========================================================

st.subheader("📋 Filtered Orders")

st.caption(
    f"Showing first 100 rows out of {len(filtered_df):,} filtered records."
)

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
    label="⬇ Download Discount Report",
    data=csv,
    file_name="Discount_Report.csv",
    mime="text/csv"
)

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.subheader("💡 Business Insights")

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
### Key Findings

• Average Profit Ratio

**{avg_profit_ratio:.2f}**

• Discount Impact

**{discount_impact:.2f}%**

• Total Orders Analysed

**{len(filtered_df):,}**
""")

with col2:

    highest = erosion.loc[
        erosion["Profit Margin (%)"].idxmax(),
        "Discount Category"
    ]

    lowest = erosion.loc[
        erosion["Profit Margin (%)"].idxmin(),
        "Discount Category"
    ]

    st.warning(f"""
### Recommendations

✅ Best Margin Category

**{highest}**

⚠ Lowest Margin Category

**{lowest}**

Review high-discount products to improve profitability.
""")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "APL Logistics • Discount Impact Dashboard • Unified Mentor Internship Project"
)