import pandas as pd
from contracts.database import get_connection


class ExportService:

    @staticmethod
    def export_csv():

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM contracts",
            conn
        )

        conn.close()

        output = "uploads/contracts.csv"

        df.to_csv(
            output,
            index=False
        )

        return output


    @staticmethod
    def export_excel():

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM contracts",
            conn
        )

        conn.close()

        output = "uploads/contracts.xlsx"

        df.to_excel(
            output,
            index=False
        )

        return output