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

st.set_page_config(
    page_title="Housing Market Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

df_raw = load_housing_data()

st.sidebar.title("🔍 Global Filters")

# Price Range
min_p = int(df_raw['price'].min()) if not df_raw.empty else 0
max_p = int(df_raw['price'].max()) if not df_raw.empty else 1000000
selected_price = st.sidebar.slider(
    "Price Range ($)",
    min_value=min_p,
    max_value=max_p,
    value=(min_p, max_p),
    step=25000,
    format="$%d"
)

# Sqft Range
min_s = int(df_raw['sqft_living'].min()) if 'sqft_living' in df_raw.columns and not df_raw.empty else 0
max_s = int(df_raw['sqft_living'].max()) if 'sqft_living' in df_raw.columns and not df_raw.empty else 10000
selected_sqft = st.sidebar.slider(
    "Living Area (Sq Ft)",
    min_value=min_s,
    max_value=max_s,
    value=(min_s, max_s),
    step=100
)

# Zipcodes
all_zips = sorted([z for z in df_raw['zipcode'].unique() if z > 0]) if 'zipcode' in df_raw.columns else []
selected_zipcodes = st.sidebar.multiselect("Zipcodes", options=all_zips, default=[])

# Bedrooms & Bathrooms
col_bed, col_bath = st.sidebar.columns(2)
with col_bed:
    bed_opts = ["All"] + sorted([int(b) for b in df_raw['bedrooms'].unique() if b >= 0]) if 'bedrooms' in df_raw.columns else ["All"]
    selected_beds = st.selectbox("Bedrooms", bed_opts)

with col_bath:
    bath_opts = ["All"] + sorted([float(b) for b in df_raw['bathrooms'].unique() if b >= 0]) if 'bathrooms' in df_raw.columns else ["All"]
    selected_baths = st.selectbox("Bathrooms", bath_opts)

# Waterfront
waterfront_filter = st.sidebar.checkbox("Waterfront Properties Only", value=False)

# Filter Logic
df_filtered = df_raw[
    (df_raw['price'] >= selected_price[0]) &
    (df_raw['price'] <= selected_price[1])
]

if 'sqft_living' in df_filtered.columns:
    df_filtered = df_filtered[
        (df_filtered['sqft_living'] >= selected_sqft[0]) &
        (df_filtered['sqft_living'] <= selected_sqft[1])
    ]

if selected_zipcodes:
    df_filtered = df_filtered[df_filtered['zipcode'].isin(selected_zipcodes)]

if selected_beds != "All":
    df_filtered = df_filtered[df_filtered['bedrooms'] == selected_beds]

if selected_baths != "All":
    df_filtered = df_filtered[df_filtered['bathrooms'] == selected_baths]

if waterfront_filter and 'waterfront' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['waterfront'] == 1]

# Main Content
st.title("🏠 Housing Market Intelligence Analytics")
st.caption("Interactive analytics derived from property sales records.")

render_kpi_cards(df_filtered)
st.markdown("---")

col_left, col_right = st.columns([1, 1])
with col_left:
    plot_geospatial_map(df_filtered)
with col_right:
    plot_price_vs_sqft(df_filtered)

col_b1, col_b2 = st.columns([1, 1])
with col_b1:
    group_col = st.selectbox("Group Distribution By:", ["bedrooms", "bathrooms", "grade", "condition"], index=0)
    plot_price_by_category(df_filtered, group_col)
with col_b2:
    plot_price_histogram(df_filtered)

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
