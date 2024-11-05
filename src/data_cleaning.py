import pandas as pd
import re

def process_dataframe(df):
    # 1. Remove Duplicates based on ID column
    df = df.drop_duplicates(subset=[df.columns[0]])  # Assume first column is ID

    # 2. Standardize capitalization in object (string) columns
    df = df.apply(lambda x: x.str.title() if x.dtype == "object" and x.name != df.columns[0] else x)


    # 3. Remove extra spaces and any quotes around values in object columns
    df = df.apply(lambda x: x.str.strip(' "\'') if x.dtype == "object" else x)

    # 4. Selectively convert strings that represent numerical data to integers
    def try_convert_column_to_int(series):
        # Remove non-numeric characters for int conversion
        def clean_and_convert(value):
            if isinstance(value, str):
                cleaned = re.sub(r'\D', '', value)  # Remove non-numeric characters
                return int(cleaned) if cleaned else None  # Convert if possible
            return value
        
        # Check if the entire column can be converted to integers
        try:
            series_cleaned = series.apply(clean_and_convert)
            # If all non-null entries in the series are integers, return converted
            if pd.api.types.is_numeric_dtype(series_cleaned.dropna()):
                return series_cleaned
        except:
            pass
        return series  # Return original if conversion not possible
    
    # Apply selective conversion to columns with potential integers
    df = df.apply(lambda col: try_convert_column_to_int(col) if col.dtype == "object" else col)
    return df


def fill_missing_with_min(df, columns):
    """
    Fill missing values in specified columns with the minimum existing value in each column.

    Parameters:
    - df (pd.DataFrame): The DataFrame to process.
    - columns (list): List of column names to apply the missing value filling.

    Returns:
    - pd.DataFrame: The DataFrame with missing values filled in the specified columns.
    """
    for col in columns:
        if col in df.columns:
            min_value = df[col].min(skipna=True)  # Find the minimum non-missing value
            df[col] = df[col].fillna(min_value)    # Fill missing values with the minimum value
    return df