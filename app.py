from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
SAMPLE_PATH = ROOT / "data" / "external" / "bank_churn_huggingface_test.csv"
PREVIEW_PDF_PATH = ROOT / "reports" / "streamlit_dashboard_report_preview.pdf"
PREVIEW_EXCEL_PATH = ROOT / "reports" / "streamlit_dashboard_export_preview.xlsx"

st.set_page_config(
    page_title="Bank Churn Risk Dashboard Demo",
    page_icon="",
    layout="wide",
)


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #172033;
            --muted: #667085;
            --line: #d9e2ec;
            --panel: #ffffff;
            --teal: #0f766e;
        }

        .stApp {
            background: linear-gradient(180deg, #eef6f8 0%, #f7f9fc 34%, #ffffff 100%);
            color: var(--ink);
        }

        section[data-testid="stSidebar"] {
            background: #0f2235;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        section[data-testid="stSidebar"] * {
            color: #eef7fb;
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1240px;
        }

        .dashboard-hero {
            background: linear-gradient(135deg, #17324d 0%, #0f766e 72%, #155e75 100%);
            color: white;
            padding: 26px 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 18px 45px rgba(15, 34, 53, 0.18);
        }

        .dashboard-hero h1 {
            font-size: 32px;
            line-height: 1.18;
            margin: 0 0 8px 0;
            letter-spacing: 0;
        }

        .dashboard-hero p {
            margin: 0;
            color: #d8eef3;
            font-size: 15px;
            max-width: 880px;
        }

        .metric-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-left: 5px solid var(--accent);
            border-radius: 8px;
            padding: 16px 16px 14px 16px;
            min-height: 112px;
            box-shadow: 0 12px 28px rgba(23, 32, 51, 0.08);
        }

        .metric-card .label {
            color: var(--muted);
            font-size: 13px;
            font-weight: 650;
            text-transform: uppercase;
        }

        .metric-card .value {
            color: var(--ink);
            font-size: 27px;
            font-weight: 800;
            margin-top: 7px;
        }

        .metric-card .hint {
            color: var(--muted);
            font-size: 12px;
            margin-top: 6px;
        }

        .section-title {
            color: var(--ink);
            font-size: 18px;
            font-weight: 700;
            margin: 24px 0 10px 0;
        }

        .locked-upload {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 8px;
            padding: 14px;
            margin-top: 10px;
        }

        .locked-upload .fake-button {
            background: rgba(255, 255, 255, 0.92);
            color: #0f2235;
            border-radius: 8px;
            padding: 9px 12px;
            font-weight: 700;
            text-align: center;
            opacity: 0.58;
            cursor: not-allowed;
            margin-top: 8px;
        }

        div[data-testid="stDownloadButton"] button {
            border-radius: 8px;
            border: 1px solid #b7c9d6;
            background: #ffffff;
            color: var(--ink);
            font-weight: 650;
        }

        div[data-testid="stDownloadButton"] button:hover {
            border-color: var(--teal);
            color: var(--teal);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 12px 28px rgba(23, 32, 51, 0.06);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, hint: str, color: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card" style="--accent: {color};">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def risk_level(probability: float) -> str:
    if probability >= 0.65:
        return "High"
    if probability >= 0.35:
        return "Medium"
    return "Low"


@st.cache_data
def load_demo_data() -> pd.DataFrame:
    df = pd.read_csv(SAMPLE_PATH).head(500).copy()
    df["churn_probability"] = (
        0.08
        + (df["Age"].clip(18, 75) - 18) / 95
        + (1 - df["IsActiveMember"]) * 0.18
        + (df["NumOfProducts"] == 1).astype(float) * 0.12
        + (df["Geography"] == "Germany").astype(float) * 0.10
        + (df["Balance"] > 90000).astype(float) * 0.08
    ).clip(0.02, 0.94)
    df["predicted_exited"] = (df["churn_probability"] >= 0.50).astype(int)
    df["risk_level"] = [risk_level(float(value)) for value in df["churn_probability"]]
    return df


def render_dashboard(scored: pd.DataFrame) -> None:
    high_risk_count = int((scored["risk_level"] == "High").sum())
    predicted_churn = int(scored["predicted_exited"].sum())
    average_probability = scored["churn_probability"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Customers", f"{len(scored):,}", "Demo records", "#2563eb")
    with col2:
        metric_card("Predicted Churn", f"{predicted_churn:,}", "Customers flagged", "#d97706")
    with col3:
        metric_card("High Risk", f"{high_risk_count:,}", "Priority segment", "#b91c1c")
    with col4:
        metric_card("Average Risk", f"{average_probability:.1%}", "Mean churn probability", "#0f766e")

    section_title("Risk Overview")
    chart_col1, chart_col2 = st.columns(2)
    risk_counts = scored["risk_level"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
    risk_fig, risk_ax = plt.subplots(figsize=(7.4, 4.1))
    risk_ax.bar(risk_counts.index, risk_counts.values, color=["#15803d", "#d97706", "#b91c1c"])
    risk_ax.set_title("Customer Count by Risk Level")
    risk_ax.set_xlabel("Risk Level")
    risk_ax.set_ylabel("Customers")
    risk_ax.spines[["top", "right"]].set_visible(False)
    chart_col1.pyplot(risk_fig, use_container_width=True)
    plt.close(risk_fig)

    geo = scored.groupby("Geography")["churn_probability"].mean().sort_values(ascending=False)
    geo_fig, geo_ax = plt.subplots(figsize=(7.4, 4.1))
    geo_ax.bar(geo.index.astype(str), geo.mul(100), color="#2563eb")
    geo_ax.set_title("Average Churn Probability by Geography")
    geo_ax.set_xlabel("Geography")
    geo_ax.set_ylabel("Probability (%)")
    geo_ax.spines[["top", "right"]].set_visible(False)
    chart_col2.pyplot(geo_fig, use_container_width=True)
    plt.close(geo_fig)

    detail_col1, detail_col2 = st.columns(2)
    activity = (
        scored.assign(activity_status=scored["IsActiveMember"].map({0: "Inactive", 1: "Active"}))
        .groupby("activity_status")["churn_probability"]
        .mean()
        .reindex(["Active", "Inactive"])
    )
    activity_fig, activity_ax = plt.subplots(figsize=(7.4, 4.1))
    activity_ax.bar(activity.index.astype(str), activity.mul(100), color=["#15803d", "#b91c1c"])
    activity_ax.set_title("Average Risk by Activity Status")
    activity_ax.set_xlabel("Activity Status")
    activity_ax.set_ylabel("Probability (%)")
    activity_ax.spines[["top", "right"]].set_visible(False)
    detail_col1.pyplot(activity_fig, use_container_width=True)
    plt.close(activity_fig)

    products = scored.groupby("NumOfProducts")["churn_probability"].mean().sort_index()
    products_fig, products_ax = plt.subplots(figsize=(7.4, 4.1))
    products_ax.bar(products.index.astype(str), products.mul(100), color="#0f766e")
    products_ax.set_title("Average Risk by Number of Products")
    products_ax.set_xlabel("Number of Products")
    products_ax.set_ylabel("Probability (%)")
    products_ax.spines[["top", "right"]].set_visible(False)
    detail_col2.pyplot(products_fig, use_container_width=True)
    plt.close(products_fig)

    section_title("Highest Risk Customers")
    display_cols = [
        "CustomerId",
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Balance",
        "NumOfProducts",
        "IsActiveMember",
        "churn_probability",
        "risk_level",
    ]
    st.dataframe(
        scored.sort_values("churn_probability", ascending=False)[display_cols].head(50),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    inject_theme()
    scored = load_demo_data()

    st.markdown(
        """
        <div class="dashboard-hero">
            <h1>Bank Customer Churn Risk Dashboard</h1>
            <p>This client demo shows how customer churn risk can be monitored through a Python and Machine Learning dashboard. The upload control is intentionally disabled in this public preview.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Demo Controls")
        st.markdown(
            """
            <div class="locked-upload">
                <strong>Import customer file</strong>
                <p style="margin: 6px 0 0 0; font-size: 13px;">Disabled in public demo.</p>
                <div class="fake-button">Upload CSV or Excel</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info("This preview uses built-in demo data. Data upload and external scoring are disabled in the public portfolio app.")

    render_dashboard(scored)

    section_title("Report Preview")
    st.download_button(
        "Download Demo PDF Preview",
        data=PREVIEW_PDF_PATH.read_bytes(),
        file_name="demo_bank_churn_dashboard.pdf",
        mime="application/pdf",
    )


if __name__ == "__main__":
    main()
