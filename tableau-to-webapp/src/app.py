import streamlit as st
import pandas as pd
from data_loader import load_housing_data
from components import (
    render_kpi_cards,
    plot_geospatial_map,
    plot_price_vs_sqft,
    plot_price_by_category,
    plot_price_histogram
)

# Page configuration
st.set_page_config(
    page_title="Housing Market Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load dataset
df_raw = load_housing_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🔍 Global Filters")

# Price Range Slider
min_price = int(df_raw['price'].min())
max_price = int(df_raw['price'].max())
selected_price = st.sidebar.slider(
    "Price Range ($)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_value),
    step=25000,
    format="$%d"
)

# Living Sqft Slider
min_sqft = int(df_raw['sqft_living'].min())
max_sqft = int(df_raw['sqft_living'].max())
selected_sqft = st.sidebar.slider(
    "Living Area (Sq Ft)",
    min_value=min_sqft,
    max_value=max_sqft,
    value=(min_sqft, max_sqft),
    step=100
)

# Zipcode Multi-select
all_zipcodes = sorted(df_raw['zipcode'].unique().tolist()) if 'zipcode' in df_raw.columns else []
selected_zipcodes = st.sidebar.multiselect(
    "Zipcodes",
    options=all_zipcodes,
    default=[]
)

# Bedrooms & Bathrooms Filter
col_bed, col_bath = st.sidebar.columns(2)
with col_bed:
    bed_options = ["All"] + sorted(df_raw['bedrooms'].unique().tolist()) if 'bedrooms' in df_raw.columns else ["All"]
    selected_beds = st.selectbox("Bedrooms", bed_options)

with col_bath:
    bath_options = ["All"] + sorted(df_raw['bathrooms'].unique().tolist()) if 'bathrooms' in df_raw.columns else ["All"]
    selected_baths = st.selectbox("Bathrooms", bath_options)

# Waterfront Toggle
waterfront_filter = st.sidebar.checkbox("Waterfront Properties Only", value=False)

# Filter Data Logic
df_filtered = df_raw[
    (df_raw['price'] >= selected_price[0]) &
    (df_raw['price'] <= selected_price[1]) &
    (df_raw['sqft_living'] >= selected_sqft[0]) &
    (df_raw['sqft_living'] <= selected_sqft[1])
]

if selected_zipcodes:
    df_filtered = df_filtered[df_filtered['zipcode'].isin(selected_zipcodes)]

if selected_beds != "All":
    df_filtered = df_filtered[df_filtered['bedrooms'] == selected_beds]

if selected_baths != "All":
    df_filtered = df_filtered[df_filtered['bathrooms'] == selected_baths]

if waterfront_filter and 'waterfront' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['waterfront'] == 1]


# --- MAIN CONTENT ---
st.title("🏠 Housing Market Intelligence Analytics")
st.caption("Interactive analytics derived from property sales records[cite: 1].")

# Top KPI Metric Cards
render_kpi_cards(df_filtered)
st.markdown("---")

# Row 1 Visuals
col_left, col_right = st.columns([1, 1])

with col_left:
    plot_geospatial_map(df_filtered)

with col_right:
    plot_price_vs_sqft(df_filtered)

# Row 2 Visuals
col_b1, col_b2 = st.columns([1, 1])

with col_b1:
    group_col = st.selectbox("Group Distribution By:", ["bedrooms", "bathrooms", "grade", "condition"], index=2)
    plot_price_by_category(df_filtered, group_col)

with col_b2:
    plot_price_histogram(df_filtered)

# Data Explorer & CSV Export
st.markdown("---")
with st.expander("📋 View & Export Filtered Property Records"):
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_housing_data.csv",
        mime="text/csv"
    )