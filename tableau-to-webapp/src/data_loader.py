import os
import re
import pandas as pd
import numpy as np
import streamlit as st

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Housing Dataset.xlsx")


def _clean_numeric(series: pd.Series) -> pd.Series:
    """Converts raw text or dirty numeric series into clean numeric floats."""
    if series is None or series.empty:
        return series
    cleaned = (
        series.astype(str)
        .str.replace(r'[\$,]', '', regex=True)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors='coerce')


def _clean_zipcode(series: pd.Series) -> pd.Series:
    """Standardizes zipcodes to 5-digit integers."""
    if series is None or series.empty:
        return series

    def parse_zip(val):
        if pd.isna(val):
            return np.nan
        val_str = str(val).strip().split('.')[0].split('-')[0]
        match = re.search(r'\b\d{5}\b', val_str)
        return int(match.group(0)) if match else np.nan

    return series.apply(parse_zip)


@st.cache_data(ttl=3600)
def load_housing_data() -> pd.DataFrame:
    """Loads, cleans, and standardizes real estate data from Housing Dataset.xlsx."""
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_excel(DATA_PATH)
        except Exception as e:
            st.error(f"❌ Error reading 'Housing Dataset.xlsx': {e}")
            st.stop()
    else:
        # Fallback synthetic data
        np.random.seed(42)
        n = 1000
        df = pd.DataFrame({
            'list_number': range(1, n + 1),
            'sold_price': np.random.normal(650000, 200000, n).clip(150000, 2500000),
            '#_bedrooms': np.random.choice([2, 3, 4, 5], n),
            '#_bathrooms': np.random.choice([1.0, 1.5, 2.0, 2.5, 3.0], n),
            'approx_sqft': np.random.normal(2100, 600, n).clip(700, 6000),
            'yr_built': np.random.randint(1950, 2023, n),
            'zipcode': np.random.choice([98001, 98002, 98003], n),
            'geo_lat': np.random.normal(47.56, 0.1, n),
            'geo_lon': np.random.normal(-122.21, 0.1, n)
        })

    # Clean headers
    df.columns = [
        str(col).strip().lower()
        .replace(' ', '_').replace('$', '').replace('(', '').replace(')', '')
        for col in df.columns
    ]

    # Map column aliases
    alias_map = {
        'sold_price': 'price',
        'sale_price': 'price',
        'list_price': 'price',
        'approx_sqft': 'sqft_living',
        'sqft': 'sqft_living',
        '#_bedrooms': 'bedrooms',
        'num_bedrooms': 'bedrooms',
        '#_bathrooms': 'bathrooms',
        'num_bathrooms': 'bathrooms',
        'geo_lat': 'lat',
        'geo_lon': 'long',
        'list_number': 'id',
        'zip': 'zipcode',
        'zip_code': 'zipcode',
        'year_built': 'yr_built'
    }
    df.rename(columns=alias_map, inplace=True)

    # Clean numeric columns
    for col in ['price', 'sqft_living', 'bedrooms', 'bathrooms', 'yr_built', 'lat', 'long']:
        if col in df.columns:
            df[col] = _clean_numeric(df[col])

    # Remove invalid prices/sqft
    df = df.dropna(subset=['price'])
    df = df[df['price'] > 0]

    if 'sqft_living' in df.columns:
        df = df[df['sqft_living'] > 0]
        df['price_per_sqft'] = df['price'] / df['sqft_living']

    # Clean bedrooms & bathrooms (Fill NaNs with 0)
    if 'bedrooms' in df.columns:
        df['bedrooms'] = df['bedrooms'].fillna(0).astype(int)
    if 'bathrooms' in df.columns:
        df['bathrooms'] = df['bathrooms'].fillna(0.0).round(1)

    # Clean Zipcodes
    if 'zipcode' in df.columns:
        df['zipcode'] = _clean_zipcode(df['zipcode'])
        df['zipcode'] = df['zipcode'].fillna(0).astype(int)

    # Waterfront Fallback
    if 'waterfront' not in df.columns:
        df['waterfront'] = 0

    # Categorical Fallbacks
    if 'grade' not in df.columns:
        df['grade'] = df['dwelling_type'] if 'dwelling_type' in df.columns else 'Standard'
    if 'condition' not in df.columns:
        df['condition'] = df['status'] if 'status' in df.columns else 'Active'
    if 'id' not in df.columns:
        df['id'] = range(1, len(df) + 1)

    return df
