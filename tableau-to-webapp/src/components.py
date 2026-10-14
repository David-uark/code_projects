import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def render_kpi_cards(df: pd.DataFrame):
    """Displays top-level property metric cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    med_price = df['price'].median() if not df.empty else 0
    avg_price_sqft = df['price_per_sqft'].mean() if not df.empty else 0
    total_props = len(df)
    avg_yr_built = int(df['yr_built'].mean()) if not df.empty and 'yr_built' in df.columns else 0

    col1.metric("Median Home Price", f"${med_price:,.0f}")
    col2.metric("Avg Price / Sq. Ft.", f"${avg_price_sqft:,.2f}")
    col3.metric("Properties Listed", f"{total_props:,}")
    col4.metric("Avg Year Built", f"{avg_yr_built}")


def plot_geospatial_map(df: pd.DataFrame):
    """Renders interactive property map centered on dataset coordinates."""
    if df.empty or 'lat' not in df.columns or 'long' not in df.columns:
        st.warning("Geospatial data unavailable for current selection.")
        return

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="long",
        color="price",
        size="sqft_living",
        color_continuous_scale=px.colors.sequential.Viridis,
        size_max=12,
        zoom=9,
        hover_name="id" if "id" in df.columns else None,
        hover_data={"price": ":$,.0f", "sqft_living": ":,", "bedrooms": True, "bathrooms": True},
        title="<b>Geospatial Property Distribution</b>"
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 35, "l": 0, "b": 0},
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_price_vs_sqft(df: pd.DataFrame):
    """Renders Price vs Square Footage scatter plot with trendline."""
    if df.empty:
        st.info("No data available.")
        return

    fig = px.scatter(
        df,
        x="sqft_living",
        y="price",
        color="grade" if "grade" in df.columns else None,
        trendline="ols",
        trendline_color_override="red",
        labels={"sqft_living": "Living Area (Sq Ft)", "price": "Sales Price ($)", "grade": "Grade"},
        title="<b>Price vs. Living Square Footage</b>"
    )
    fig.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",",
        xaxis_tickformat=",",
        margin={"r": 10, "t": 35, "l": 10, "b": 10},
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_price_by_category(df: pd.DataFrame, category_col: str):
    """Renders price distribution violin plot grouped by selected category."""
    if df.empty or category_col not in df.columns:
        st.info("Category data unavailable.")
        return

    fig = px.violin(
        df,
        x=category_col,
        y="price",
        box=True,
        points=False,
        color=category_col,
        labels={category_col: category_col.replace('_', ' ').title(), "price": "Sales Price ($)"},
        title=f"<b>Price Distribution by {category_col.replace('_', ' ').title()}</b>"
    )
    fig.update_layout(
        showlegend=False,
        yaxis_tickprefix="$",
        yaxis_tickformat=",",
        margin={"r": 10, "t": 35, "l": 10, "b": 10},
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_price_histogram(df: pd.DataFrame):
    """Renders sales price frequency histogram."""
    if df.empty:
        return

    fig = px.histogram(
        df,
        x="price",
        nbins=40,
        title="<b>Sales Price Distribution Frequency</b>",
        labels={"price": "Sales Price ($)"},
        color_discrete_sequence=["#2E86C1"]
    )
    fig.update_layout(
        xaxis_tickprefix="$",
        xaxis_tickformat=",",
        yaxis_title="Property Count",
        margin={"r": 10, "t": 35, "l": 10, "b": 10},
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)