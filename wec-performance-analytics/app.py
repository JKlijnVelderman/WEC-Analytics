
from pathlib import Path

import pandas as pd
import streamlit as st



# CONFIGURATION
st.set_page_config(
    page_title="WEC Performance Analytics",
    page_icon="🏎️",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parent

CLASSIFICATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "spa_2025_race_classification.csv"
)


# HEADER
st.title("WEC Performance Analytics")

st.caption(
    "2025 TotalEnergies 6 Hours of Spa-Francorchamps"
)

st.divider()

# DATA GATHERING
if not CLASSIFICATION_FILE.exists():

    st.warning(
        "Race classification not yet available. "
        "Run scripts/01_validate_source.py first."
    )

    st.stop()
results = pd.read_csv(CLASSIFICATION_FILE)

# SIDEBAR
st.sidebar.header("Analysis Configuration")

classes = sorted(
    results["car_class"].dropna().unique()
)

selected_class = st.sidebar.selectbox(
    "Select class",
    classes
)

filtered_results = results[
    results["car_class"] == selected_class
]

# OVERVIEW METRICS
col1, col2, col3 = st.columns(3)

col1.metric(
    "Cars in class",
    len(filtered_results)
)

col2.metric(
    "Race class",
    selected_class
)

col3.metric(
    "WRT entries",
    filtered_results["team"]
    .str.contains("WRT", case=False, na=False)
    .sum()
)

# CLASSIFICATION 
st.subheader("Race Classification")

st.dataframe(
    filtered_results,
    use_container_width=True,
    hide_index=True
)


st.divider()

st.subheader("Engineering Analysis")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Race Pace",
    "Driver Analysis",
    "Stints",
    "Pit Stops",
    "Race Strategy"
])

with tab1:
    st.info("Lap-by-lap analysis – .")

with tab2:
    st.info("Driver performance analysis – .")

with tab3:
    st.info("Stint analysis – .")

with tab4:
    st.info("Pit-stop analysis – .")

with tab5:
    st.info("Race strategy analysis – .")
