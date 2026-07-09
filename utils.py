import pandas as pd
import streamlit as st

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("APL_Logistics.csv", encoding="latin1")
    return df


# -----------------------------
# Sidebar Filters
# -----------------------------
def apply_filters(df):

    st.sidebar.header("🔍 Dashboard Filters")

    market = st.sidebar.multiselect(
        "Market",
        sorted(df["Market"].dropna().unique()),
        default=sorted(df["Market"].dropna().unique())
    )

    segment = st.sidebar.multiselect(
        "Customer Segment",
        sorted(df["Customer Segment"].dropna().unique()),
        default=sorted(df["Customer Segment"].dropna().unique())
    )

    category = st.sidebar.multiselect(
        "Category",
        sorted(df["Category Name"].dropna().unique()),
        default=sorted(df["Category Name"].dropna().unique())
    )

    shipping = st.sidebar.multiselect(
        "Shipping Mode",
        sorted(df["Shipping Mode"].dropna().unique()),
        default=sorted(df["Shipping Mode"].dropna().unique())
    )

    filtered_df = df[
        (df["Market"].isin(market)) &
        (df["Customer Segment"].isin(segment)) &
        (df["Category Name"].isin(category)) &
        (df["Shipping Mode"].isin(shipping))
    ]

    return filtered_df


# -----------------------------
# KPI Calculator
# -----------------------------
def calculate_kpis(df):

    total_sales = df["Sales"].sum()

    total_profit = df["Order Profit Per Order"].sum()

    total_orders = len(df)

    total_customers = df["Customer Id"].nunique()

    profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0 else 0
    )

    avg_discount = (
        df["Order Item Discount Rate"].mean() * 100
    )

    return {
        "sales": total_sales,
        "profit": total_profit,
        "orders": total_orders,
        "customers": total_customers,
        "margin": profit_margin,
        "discount": avg_discount
    }