import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data(file_path):
    df = pd.read_csv(file_path)

    # Normalize columns
    df.columns = df.columns.str.strip()

    # Convert dates
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
# MAIN
# -----------------------------
if __name__ == "__main__":
    file_path = "Eppix_merged_TT_orders.csv-success.csv-success.csv"

    df = load_data(file_path)

    kpis = calculate_kpis(df)
    breakdown_df = source_breakdown(df)

    print("\n===== OVERALL KPI =====")
    for k, v in kpis.items():
        print(f"{k}: {v}")

    print("\n===== SOURCE BREAKDOWN =====")
    print(breakdown_df)