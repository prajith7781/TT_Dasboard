import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    df['sourceTransDate'] = pd.to_datetime(df['sourceTransDate'], errors='coerce')
    df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
    df['endDate'] = pd.to_datetime(df['endDate'], errors='coerce')

    return df


# -----------------------------
# KPI CALCULATIONS
# -----------------------------
def calculate_kpis(df):
    total_extracted = len(df)
    total_loaded = df['piId'].notna().sum()
    total_succeeded = df[df['status'].str.lower() == 'completed'].shape[0]
    total_failed = total_loaded - total_succeeded

    load_rate = (total_loaded / total_extracted) * 100 if total_extracted else 0
    success_rate = (total_succeeded / total_loaded) * 100 if total_loaded else 0

    return {
        "total_extracted": total_extracted,
        "total_loaded": total_loaded,
        "total_succeeded": total_succeeded,
        "total_failed": total_failed,
        "load_rate": round(load_rate, 2),
        "success_rate": round(success_rate, 2)
    }


# -----------------------------
# SOURCE BREAKDOWN
# -----------------------------
def source_breakdown(df):
    breakdown = []

    grouped = df.groupby('sourceRequest')

    for name, group in grouped:
        extracted = len(group)
        loaded = group['piId'].notna().sum()
        succeeded = group[group['status'].str.lower() == 'completed'].shape[0]
        failed = loaded - succeeded

        load_rate = (loaded / extracted) * 100 if extracted else 0
        success_rate = (succeeded / loaded) * 100 if loaded else 0

        breakdown.append({
            "sourceRequest": name,
            "extracted": extracted,
            "loaded": loaded,
            "succeeded": succeeded,
            "failed": failed,
            "load_rate": round(load_rate, 2),
            "success_rate": round(success_rate, 2)
        })

    return pd.DataFrame(breakdown)


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 ILULA & Eppix → TT Dashboard")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = load_data(file)

    kpis = calculate_kpis(df)
    breakdown = source_breakdown(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Extracted", kpis["total_extracted"])
    col2.metric("Total Loaded (TT)", f"{kpis['total_loaded']} ({kpis['load_rate']}%)")
    col3.metric("Total Succeeded", f"{kpis['total_succeeded']} ({kpis['success_rate']}%)")
    col4.metric("Total Failed", kpis["total_failed"])

    st.markdown("---")
    st.subheader("Source Breakdown")
    st.dataframe(breakdown, use_container_width=True)