# Bank Customer Churn Risk Dashboard Demo

This is the public client demo version of the Bank Customer Churn Risk Dashboard.

The dashboard displays prepared demo data, risk indicators, customer churn charts, high-risk customer tables, and downloadable demo reports. The import/upload feature is intentionally disabled in this public preview so visitors can inspect the dashboard experience without running private data through the model.

## What Visitors Can See

- Customer churn risk overview
- High-risk customer count
- Average churn probability
- Risk distribution by level
- Average risk by geography
- Average risk by activity status
- Average risk by number of products
- High-risk customer table
- Demo Excel/PDF/CSV export

## What Is Disabled

The file import button is shown as a locked demo control. Visitors cannot upload their own CSV or Excel data in this public version.

## Run the Demo

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Note

This folder is intended for public portfolio presentation. The full private version includes live CSV/Excel import and model scoring.
