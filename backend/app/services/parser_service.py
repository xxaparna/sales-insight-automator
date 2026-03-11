import pandas as pd
import io


def parse_sales_file(file_bytes: bytes, filename: str):
    try:

        # detect file type
        if filename.lower().endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))

        stats = {
            "total_rows": len(df),
            "columns": list(df.columns),
            "data_preview": df.head(5).to_string(),
        }

        numeric_cols = df.select_dtypes(include="number").columns

        for col in numeric_cols:
            stats[f"{col}_total"] = float(df[col].sum())
            stats[f"{col}_mean"] = round(float(df[col].mean()), 2)
            stats[f"{col}_max"] = float(df[col].max())

        cat_cols = df.select_dtypes(include="object").columns

        for col in list(cat_cols)[:3]:
            stats[f"{col}_top"] = df[col].value_counts().head(3).to_dict()

        return stats

    except Exception as e:
        raise ValueError(f"Failed to parse file: {str(e)}")