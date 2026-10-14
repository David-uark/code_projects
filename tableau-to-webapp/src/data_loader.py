import os
import pandas as pd
import numpy as np
import streamlit as st

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Housing Dataset.xlsx")

@st.cache_data(ttl=3600)
def load_housing_data() -> pd.DataFrame:
    """Loads and standardizes property data from Housing Dataset.xlsx."""
    if os.path.exists(DATA_PATH):
        df = pd.read_excel(DATA_PATH)
    else:
        # Fallback dataset generator for development/testing
        np.random.seed(42)
        n = 1000
        df = pd.DataFrame({
            'id': range(1, n + 1),
            'price': np.random.normal(650000, 200000, n).clip(150000, 2500000),
            'bedrooms': np.random.choice([2, 3, 4, 5], n, p=[0.2, 0.5, 0.2, 0.1]),
            'bathrooms': np.random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5], n),
            'sqft_living': np.random.normal(2100, 600, n).clip(700, 6000),
            'sqft_lot': np.random.normal(7500, 2000, n).clip(1000, 20000),
            'floors': np.random.choice([1.0, 1.5, 2.0, 2.5], n),
            'waterfront': np.random.choice([0, 1], n, p=[0.95, 0.05]),
            'view': np.random.choice([0, 1, 2, 3, 4], n),
            'condition': np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.1, 0.6, 0.2, 0.05]),
            'grade': np.random.choice([5, 6, 7, 8, 9, 10, 11], n, p=[0.05, 0.1, 0.4, 0.3, 0.1, 0.03, 0.02]),
            'yr_built': np.random.randint(1950, 2023, n),
            'zipcode': np.random.choice([98001, 98002, 98003, 98004, 98005, 98033, 98052], n),
            'lat': np.random.normal(47.56, 0.1, n),
            'long': np.random.normal(-122.21, 0.1, n)
        })

    # Standardize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Derived calculated fields
    if 'price' in df.columns and 'sqft_living' in df.columns:
        df['price_per_sqft'] = df['price'] / df['sqft_living']

    return df