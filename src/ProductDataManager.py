import os
import polars as pl
from settings import BASE_DIR, EXCEL_CONFIGS

class ExcelManager:
    """
    Class to manage the Excel files containing product data.
    Handles reading and writing Excel files with Polars from standardized templates.
    """

    def __init__(self):
        self.settings = EXCEL_CONFIGS
        self.current_directory = BASE_DIR / self.settings["product_file_directory"]
        os.chdir(self.current_directory)

    def get_file_names(self):
        return [
            os.path.join(self.current_directory, f)
            for f in os.listdir(self.current_directory)
            if f.endswith(".xlsx")
        ]

    def validate_data(self, df):
        # Check for missing required columns
        for col in self.settings["required_columns"]:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Add more validation checks as needed

    def read_excel_files(self, file_names):
        dfs = []
        for file_name in file_names:
            df = pl.read_excel(
                file_name,
                sheet_name=self.settings["sheet_name"],
                read_options={"header_row": self.settings["header_row"]},
            )
            df = df.with_columns(
                [pl.col(col).cast(dtype) for col, dtype in self.settings["column_types"].items()]
            )
            self.validate_data(df)
            dfs.append(df)
        return pl.concat(dfs)

    def write_to_csv(self, df):
        output_path = os.path.join(self.current_directory, self.settings["output_file"])
        try:
            df.write_csv(output_path)
            print(f"Combined dataframe written to {output_path}")
        except Exception as e:
            print(f"Error writing to {output_path}: {e}")

    def process_files(self):
        file_names = self.get_file_names()
        combined_df = self.read_excel_files(file_names)
        self.write_to_csv(combined_df)

# Create an instance of ExcelManager and process the files
excel_manager = ExcelManager()
excel_manager.process_files()