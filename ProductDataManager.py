import os
import json
import polars as pl


class ExcelExporter:
    def __init__(self, json_file):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.product_file_directory = os.path.join(self.current_directory, 'product_file')
        
        with open(os.path.join(self.current_directory, 'headers.json')) as f:
            self.headers = json.load(f)

    def get_file_names(self):
        return [os.path.join(self.product_file_directory, f) for f in os.listdir(self.product_file_directory) if f.endswith('.xlsx')]

    def validate_data(self, df):
        required_columns = [
            "item_type", "manufacturer", "manufacturer_part_number", "commercial_price",
            "delivery_days", "lead_time_code", "fob_us", "fob_ak", "fob_hi", "fob_pr"
        ]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Add more validation checks as needed

    def get_product_df(self, file_names, header_key):
        dfs = []
        for file_name in file_names:
            df = pl.read_excel(
                file_name,
                sheet_name="PRODUCTS",
                read_options={"header_row": 1},
            )

            df = df.with_columns([
                pl.col(col).cast(pl.Utf8) if col in ["item_type", "manufacturer", "manufacturer_part_number", "vendor_part_number", "item_name", "item_description", "uom", "quantity_unit_uom", "mfc_name", "country_of_origin", "lead_time_code", "fob_us", "fob_ak", "fob_hi", "fob_pr", "nsn", "upc", "unspsc", "default_photo", "photo_2", "photo_3", "photo_4", "product_url", "warranty_unit_of_time", "physical_uom", "product_info_code", "url_508", "hazmat"] else
                pl.col(col).cast(pl.Float64) if col in ["recycled_content_percent", "commercial_price", "mfc_price", "govt_price_no_fee", "govt_price_with_fee", "sale_price_with_fee", "length", "width", "height", "weight_lbs", "dealer_cost", "mfc_markup_percentage", "govt_markup_percentage"] else
                pl.col(col).cast(pl.Int64) if col in ["quantity_per_pack", "delivery_days", "warranty_period"] else
                pl.col(col).cast(pl.Date) if col in ["start_date", "stop_date"] else
                pl.col(col)
                for col in self.headers[header_key]
            ])

            self.validate_data(df)
            dfs.append(df)

        combined_df = pl.concat(dfs)
        output_path = os.path.join(self.current_directory, 'master_df.csv')
        try:
            combined_df.write_csv(output_path)
            print(f"Combined dataframe written to {output_path}")
        except Exception as e:
            print(f"Error writing to {output_path}: {e}")
