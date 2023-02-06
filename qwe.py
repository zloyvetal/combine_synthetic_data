XLSX_FILE = "test_data.xlsx"
from typing import Any
import pandas as pd


def xlsx_to_dict(xlsx_file, sheet_number) -> list[dict[str: Any]]:
    if sheet_number == 2:
        df = pd.read_excel(xlsx_file, sheet_name=sheet_number)
        df2 = df.melt(id_vars="Opportunity Id", var_name="date", value_name="value")
        return df2.sort_values("Opportunity Id").to_dict(orient="records")

    df = pd.read_excel(xlsx_file, sheet_name=sheet_number)
    dict_data = df.to_dict(orient="records")

    return dict_data


data = xlsx_to_dict(XLSX_FILE, 2)
