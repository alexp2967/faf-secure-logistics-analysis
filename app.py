import streamlit as st
import pandas as pd
import plotly.express as px
import ollama

st.set_page_config(page_title="FAF Freight Analysis", layout="wide")
st.title("🚛 U.S. Freight Flow Analysis")
st.caption("Source: Bureau of Transportation Statistics — FAF 5.7.1 (2018–2024)")

MODE_MAP = {
    1: "Truck", 2: "Rail", 3: "Water",
    4: "Air", 5: "Pipeline", 6: "Other/Unknown",
    7: "Multiple Modes", 8: "Mail"
}
TRADE_MAP = {1: "Domestic", 2: "Import", 3: "Export"}

COMMODITY_MAP = {
    1: "Live Animals/Fish", 2: "Cereal Grains", 3: "Agricultural Products",
    4: "Animal Feed", 5: "Meat/Seafood", 6: "Milled Grain Products",
    7: "Other Foodstuffs", 8: "Alcoholic Beverages", 9: "Tobacco",
    10: "Building Stone", 11: "Natural Sands", 12: "Gravel",
    13: "Nonmetallic Minerals", 14: "Metallic Ores", 15: "Coal",
    16: "Crude Petroleum", 17: "Gasoline", 18: "Fuel Oils",
    19: "Natural Gas", 20: "Basic Chemicals", 21: "Pharmaceutical Products",
    22: "Fertilizers", 23: "Chemical Products", 24: "Plastics/Rubber",
    25: "Logs/Wood", 26: "Wood Products", 27: "Newsprint/Paper",
    28: "Paper Products", 29: "Printed Products", 30: "Textiles/Leather",
    31: "Nonmetal Mineral Products", 32: "Base Metals",
    33: "Metal Products", 34: "Machinery", 35: "Electronics",
    36: "Motorized Vehicles", 37: "Transport Equipment",
    38: "Precision Instruments", 39: "Furniture", 40: "Misc Products",
    41: "Waste/Scrap", 43: "Mixed Freight"
}

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/faf_tiny.csv")
    df["mode_label"] = df["dms_mode"].map(MODE_MAP)
    df["trade_label"] = df["trade_type"].map(TRADE_MAP)
    df["commodity_label"] = df["sctg2"].map(COMMODITY_MAP)
    return df

df = load_data()

def get_insight(prompt):
    with st.spinner("Generating AI insight..."):
        response = ollama.chat(
            model="phi3",
            messages=[{
                "role": "user",
                "content": f"""You are a freight data analyst for military logistics.
Use ONLY the data provided. Do not add information not in the data.
Write exactly 2 professional sentences summarizing the key insight:
{prompt}"""
            }]
        )
    return response["message"]["content"]

# --- Sidebar ---
st.sidebar.header("🔍 Filters")
years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("Year(s)", years, default=years)
modes = ["All"] + sorted(df["mode_label"].dropna().unique())
selected_mode = st.sidebar.selectbox("Transport Mode", modes)
trades = ["All"] + sorted(df["trade_label"].dropna().unique())
selected_trade = st.sidebar.selectbox("Trade Type", trades)

filtered = df[df["year"].isin(selected_years)]
if selected_mode != "All":
    filtered = filtered[filtered["mode_label"] == selected_mode]
if selected_trade != "All":
    filtered = filtered[filtered["trade_label"] == selected_trade]

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Trend Analysis",
    "📦 Commodity Intelligence",
    "🌐 Trade Flow"
])

# ── TAB 1: OVERVIEW ──────────────────────────────────────────
with tab1:
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tons (k)", f"{filtered['tons'].sum():,.0f}")
    col2.metric("Value ($M)", f"{filtered['value'].sum():,.0f}")
    col3.metric("Ton-Miles (M)", f"{filtered['tmiles'].sum():,.0f}")

    st.divider()

    st.subheader("🚛 Freight Volume by Transport Mode")
    mode_df = filtered.groupby("mode_label")[["tons", "value"]].sum().reset_index()
    mode_df["value_per_ton"] = (mode_df["value"] / mode_df["tons"]).round(2)
    metric = st.radio("View by", ["tons", "value", "value_per_ton"], horizontal=True)
    fig1 = px.bar(mode_df, x="mode_label", y=metric, color="mode_label",
                  labels={"mode_label": "Mode", "value_per_ton": "Value Per Ton ($M)"})
    st.plotly_chart(fig1, use_container_width=True)

    if st.button("🤖 Generate Insight — Mode"):
        top = mode_df.nlargest(3, "tons")[["mode_label", "tons", "value_per_ton"]].to_string(index=False)
        st.info(get_insight(f"Top freight modes by tonnage and value per ton:\n{top}"))

# ── TAB 2: TREND ANALYSIS ────────────────────────────────────
with tab2:
    st.subheader("📈 Freight Volume 2018–2024")

    time_df = filtered.groupby("year")[["tons", "value", "tmiles"]].sum().reset_index()

    fig2 = px.line(time_df, x="year", y="tons", markers=True,
                   labels={"tons": "Tons (thousands)", "year": "Year"},
                   title="Total Freight Tons by Year")

    # Highlight COVID year
    fig2.add_vline(x=2020, line_dash="dash", line_color="red",
                   annotation_text="COVID-19", annotation_position="top right")

    st.plotly_chart(fig2, use_container_width=True)

    # Year over year change
    time_df["yoy_change"] = time_df["tons"].pct_change() * 100
    st.subheader("Year-Over-Year Change (%)")
    fig3 = px.bar(time_df, x="year", y="yoy_change",
                  color="yoy_change",
                  color_continuous_scale=["red", "gray", "green"],
                  labels={"yoy_change": "% Change", "year": "Year"})
    st.plotly_chart(fig3, use_container_width=True)

    if st.button("🤖 Generate Insight — Trends"):
        trend = time_df[["year", "tons", "yoy_change"]].to_string(index=False)
        st.info(get_insight(f"Freight volume trend 2018-2024 with year over year change:\n{trend}"))

# ── TAB 3: COMMODITY INTELLIGENCE ────────────────────────────
with tab3:
    st.subheader("📦 Top 10 Commodities by Tonnage")

    comm_tons = filtered.groupby("commodity_label")["tons"].sum().nlargest(10).reset_index()
    fig4 = px.bar(comm_tons, x="tons", y="commodity_label",
                  orientation="h",
                  labels={"tons": "Tons (thousands)", "commodity_label": "Commodity"},
                  color="tons", color_continuous_scale="blues")
    fig4.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("💰 Top 10 Commodities by Value")
    comm_val = filtered.groupby("commodity_label")["value"].sum().nlargest(10).reset_index()
    fig5 = px.bar(comm_val, x="value", y="commodity_label",
                  orientation="h",
                  labels={"value": "Value ($M)", "commodity_label": "Commodity"},
                  color="value", color_continuous_scale="greens")
    fig5.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig5, use_container_width=True)

    if st.button("🤖 Generate Insight — Commodities"):
        tons_str = comm_tons.head(5).to_string(index=False)
        val_str = comm_val.head(5).to_string(index=False)
        st.info(get_insight(
            f"Top 5 commodities by tonnage:\n{tons_str}\n\nTop 5 by value:\n{val_str}"
        ))

# ── TAB 4: TRADE FLOW ────────────────────────────────────────
with tab4:
    st.subheader("🌐 Trade Type Distribution")

    col1, col2 = st.columns(2)

    with col1:
        trade_df = filtered.groupby("trade_label")[["tons", "value"]].sum().reset_index()
        fig6 = px.pie(trade_df, names="trade_label", values="tons",
                      hole=0.4, title="Share by Tonnage")
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        fig7 = px.pie(trade_df, names="trade_label", values="value",
                      hole=0.4, title="Share by Value")
        st.plotly_chart(fig7, use_container_width=True)

    st.subheader("Value Per Ton by Trade Type")
    trade_df["value_per_ton"] = (trade_df["value"] / trade_df["tons"]).round(2)
    fig8 = px.bar(trade_df, x="trade_label", y="value_per_ton",
                  color="trade_label",
                  labels={"value_per_ton": "Value Per Ton ($M)", "trade_label": "Trade Type"})
    st.plotly_chart(fig8, use_container_width=True)

    if st.button("🤖 Generate Insight — Trade Flow"):
        trade_str = trade_df.to_string(index=False)
        st.info(get_insight(
            f"Trade flow breakdown by type, tonnage, value and value per ton:\n{trade_str}"
        ))