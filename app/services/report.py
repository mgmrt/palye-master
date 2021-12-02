from io import BytesIO

import pandas as pd


class ReportService:
    @staticmethod
    def create_excel_file(data):
        buffer = BytesIO()
        df = pd.DataFrame(data)
        df.to_excel(buffer, sheet_name='Palye Rapor')

        return buffer.getvalue()
