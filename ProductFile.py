import os
import polars as pl

# Get the current directory of the script
current_directory = os.path.dirname(os.path.realpath(__file__))

# Change the working directory to the location of the script
os.chdir(current_directory)

# Define the directory containing the Excel files
product_file_directory = os.path.join(current_directory, 'product_file')

# Get all Excel file names from the product_file directory
file_names = [os.path.join(product_file_directory, f) for f in os.listdir(product_file_directory) if f.endswith('.xlsx')]

def validate_data(df):
    # Check for missing required columns
    required_columns = [
        "item_type", "manufacturer", "manufacturer_part_number", "commercial_price",
        "delivery_days", "lead_time_code", "fob_us", "fob_ak", "fob_hi", "fob_pr"
    ]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Add validation checks here
    # if df['recycled_content_percent'].min() < 0 or df['recycled_content_percent'].max() > 1:
    #     raise ValueError("Recycled Content Percent must be between 0 and 1")
    # if df['quantity_per_pack'].min() <= 0:
    #     raise ValueError("Quantity per Pack must be a positive number")
    # if df['commercial_price'].min() <= 0:
    #     raise ValueError("Commercial Price must be a positive number")
    # if df['delivery_days'].min() <= 0:
    #     raise ValueError("Delivery Days must be a positive number")
    # if df['start_date'].strptime(pl.Date, "%m/%d/%Y").is_null().any():
    #     raise ValueError("Start Date must be in format 'mm/dd/yyyy'")
    # if df['stop_date'].strptime(pl.Date, "%m/%d/%Y").is_null().any():
    #     raise ValueError("Stop Date must be in format 'mm/dd/yyyy'")
    # if df['warranty_period'].min() <= 0 or df['warranty_period'].max() > 999:
    #     raise ValueError("Warranty Period must be a positive number and may not exceed 999")
    # Add more validation checks as needed

def get_product_df(file_names):
    # Initialize a list to hold the dataframes
    dfs = []

    # Load each sheet with the specified header row (2nd row, index 1)
    for file_name in file_names:
        df = pl.read_excel(
                file_name,
                sheet_name="PRODUCTS",
                read_options={"header_row": 1},
                )

        # Cast columns to consistent data types
        df = df.with_columns([
            pl.col("item_type").cast(pl.Utf8),
            pl.col("manufacturer").cast(pl.Utf8),
            pl.col("manufacturer_part_number").cast(pl.Utf8),
            pl.col("vendor_part_number").cast(pl.Utf8),
            pl.col("item_name").cast(pl.Utf8),
            pl.col("item_description").cast(pl.Utf8),
            pl.col("recycled_content_percent").cast(pl.Float64),
            pl.col("uom").cast(pl.Utf8),
            pl.col("quantity_per_pack").cast(pl.Int64),
            pl.col("quantity_unit_uom").cast(pl.Utf8),
            pl.col("commercial_price").cast(pl.Float64),
            pl.col("mfc_name").cast(pl.Utf8),
            pl.col("mfc_price").cast(pl.Float64),
            pl.col("govt_price_no_fee").cast(pl.Float64),
            pl.col("govt_price_with_fee").cast(pl.Float64),
            pl.col("country_of_origin").cast(pl.Utf8),
            pl.col("delivery_days").cast(pl.Int64),
            pl.col("lead_time_code").cast(pl.Utf8),
            pl.col("fob_us").cast(pl.Utf8),
            pl.col("fob_ak").cast(pl.Utf8),
            pl.col("fob_hi").cast(pl.Utf8),
            pl.col("fob_pr").cast(pl.Utf8),
            pl.col("nsn").cast(pl.Utf8),
            pl.col("upc").cast(pl.Utf8),
            pl.col("unspsc").cast(pl.Utf8),
            pl.col("sale_price_with_fee").cast(pl.Float64),
            pl.col("start_date").cast(pl.Date),
            pl.col("stop_date").cast(pl.Date),
            pl.col("default_photo").cast(pl.Utf8),
            pl.col("photo_2").cast(pl.Utf8),
            pl.col("photo_3").cast(pl.Utf8),
            pl.col("photo_4").cast(pl.Utf8),
            pl.col("product_url").cast(pl.Utf8),
            pl.col("warranty_period").cast(pl.Int64),
            pl.col("warranty_unit_of_time").cast(pl.Utf8),
            pl.col("length").cast(pl.Float64),
            pl.col("width").cast(pl.Float64),
            pl.col("height").cast(pl.Float64),
            pl.col("physical_uom").cast(pl.Utf8),
            pl.col("weight_lbs").cast(pl.Float64),
            pl.col("product_info_code").cast(pl.Utf8),
            pl.col("url_508").cast(pl.Utf8),
            pl.col("hazmat").cast(pl.Utf8),
            pl.col("dealer_cost").cast(pl.Float64),
            pl.col("mfc_markup_percentage").cast(pl.Float64),
            pl.col("govt_markup_percentage").cast(pl.Float64),
        ])

        # Validate data
        validate_data(df)

        dfs.append(df)

    # Combine the dataframes into one
    combined_df = pl.concat(dfs)

    # Write the final dataframe to a CSV file
    output_path = os.path.join(current_directory, 'master_df.csv')
    try:
        combined_df.write_csv(output_path)
        print(f"Combined dataframe written to {output_path}")
    except Exception as e:
        print(f"Error writing to {output_path}: {e}")

# Call the function with the collected file names
get_product_df(file_names)


# Columns for product file

PRODUCT_FILE_COLUMNS = [
    "item_type",
    "manufacturer",
    "manufacturer_part_number"
    "vendor_part_number",
    "item_name",
    "item_description",
    "recycled_content_percent",
    "uom",
    "quantity_per_pack",
    "quantity_unit_uom",
    "commercial_price",
    "mfc_name",
    "mfc_price",
    "govt_price_no_fee",
    "govt_price_with_fee",
    "country_of_origin",
    "delivery_days",
    "lead_time_code",
    "fob_us",
    "fob_ak",
    "fob_hi",
    "fob_pr",
    "nsn",
    "upc",
    "unspsc",
    "sale_price_with_fee",
    "start_date",
    "stop_date",
    "default_photo",
    "photo_2",
    "photo_3",
    "photo_4",
    "product_url",
    "warranty_period",
    "warranty_unit_of_time",
    "length",
    "width",
    "height",
    "physical_uom",
    "weight_lbs",
    "product_info_code",
    "url_508",
    "hazmat",
    "dealer_cost",
    "mfc_markup_percentage",
    "govt_markup_percentage"
]