import pandas as pd
from typing import Union, List


class MissingColumns(Exception):
    """Exception to handle missing columns in DataFrames"""
    def __init__(self, columns: str):
        self.message = f"The following columns are not found in the DataFrame: {columns}"
        super().__init__(self.message)

def check_for_required_columns(columns_used: Union[str, List[str]], columns_available: List[str]) -> None:
    """
        Check that all required column names are found in the list of available column names
        Raise a MissingColumns error if any are not found
    """
    if type(columns_used) != list:
        # Convert primitive type to list of a single item
        columns_used = [columns_used]
    # Check if any items from used list are not in the available list
    missing_columns = [x for x in columns_used if x not in columns_available]
    if len(missing_columns) > 0:
        raise MissingColumns(str(missing_columns))

def calculate_profit_by_order(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate profit for each order in the DataFrame"""
    check_for_required_columns(['List Price', 'Discount Percent', 'cost price', 'Quantity'], orders_df.columns.to_list())
    orders_df['Profit'] = orders_df.apply(
        lambda x: round((x['List Price'] * (1.0 - x['Discount Percent'] / 100.0) - x['cost price']) * x['Quantity'], 2),
        axis=1
    )
    return orders_df

def calculate_most_profitable_region(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the most profitable region and its profit"""
    check_for_required_columns('Region', orders_df.columns.to_list())
    # Determine the Profit/Order
    orders_df = calculate_profit_by_order(orders_df)
    # Aggregate on Region using Profit and sort to put max Profit as first row
    profit_by_region = orders_df.groupby('Region', as_index=False).agg({'Profit': 'sum'}).sort_values(by='Profit', ascending=False)
    # Note: This will only return 1 row. If there is a "tie" only the first row will be returned
    max_region_profit = profit_by_region.loc[[0]]
    return max_region_profit

def find_most_common_ship_method(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Find the most common shipping method for each Category"""
    check_for_required_columns(['Category', 'Ship Mode'], orders_df.columns.to_list())
    # Aggregate count of orders on Category, Ship Mode
    ship_mode_counts = orders_df.groupby(['Category','Ship Mode'], as_index=False).agg(
            Order_count=('Order Id', 'count')
        )
    # Utilize groupby() to get id of max Order_count for each Category
    # Note: This will only return 1 row per category. If there is a "tie" the first listed row is selected
    max_ship_method_category = ship_mode_counts.loc[
            ship_mode_counts.groupby('Category')['Order_count'].idxmax()
        ].reset_index(drop=True)
    return max_ship_method_category

def find_number_of_order_per_category(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Find the number of orders for each Category and Sub Category"""
    check_for_required_columns(['Category', 'Sub Category'], orders_df.columns.to_list())
    # Aggregate count of orders over Category and Sub Category
    category_subcategory_counts = orders_df.groupby(['Category', 'Sub Category'], as_index=False).agg(
            Orders=('Order Id', 'count')
        )
    return category_subcategory_counts
