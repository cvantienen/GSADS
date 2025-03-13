import os
import polars as pl
from .ProductDataManager import ProductDataManager 

# Get the current directory of the script
current_directory = os.path.dirname(os.path.realpath(__file__))
# Change the working directory to the location of the script
os.chdir(current_directory)
# Define the directory containing the Excel files
product_file_directory = os.path.join(current_directory, EXCEL_SETTINGS["product_file_directory"])

# Get all Excel file names from the product_file directory
file_names = [
    os.path.join(product_file_directory, f)
    for f in os.listdir(product_file_directory)
    if f.endswith(".xlsx")
]

def validate_data(df):
    # Check for missing required columns
    for col in EXCEL_SETTINGS["required_columns"]:
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
            sheet_name=EXCEL_SETTINGS["sheet_name"],
            read_options={"header_row": EXCEL_SETTINGS["header_row"]},
        )

        # Cast columns to consistent data types
        df = df.with_columns(
            [pl.col(col).cast(dtype) for col, dtype in EXCEL_SETTINGS["column_types"].items()]
        )

        # Validate data
        validate_data(df)

        dfs.append(df)

    # Combine the dataframes into one
    combined_df = pl.concat(dfs)

    # Write the final dataframe to a CSV file
    output_path = os.path.join(current_directory, EXCEL_SETTINGS["output_file"])
    try:
        combined_df.write_csv(output_path)
        print(f"Combined dataframe written to {output_path}")
    except Exception as e:
        print(f"Error writing to {output_path}: {e}")

# Call the function with the collected file names
get_product_df(file_names)