import pandas as pd
"Complete thes functions or write your own to perform the following tasks"

def calculate_profit_by_order(orders_df: pd.DataFrame) -> pd.DataFrame:
    "Calculate profit for each order in the DataFrame"
    orders_df['Profit'] = orders_df.apply(
        lambda x: (x['List Price'] * (1 - x['Discount Percent'] / 100) - x['cost price']) * x['Quantity'],
        axis=1
    )
    return orders_df

def calculate_most_profitable_region(orders_df: pd.DataFrame) -> dict:
    "Calculate the most profitable region and its profit"
    # Determine the Profit/Order
    orders_df = calculate_profit_by_order(orders_df)
    # Aggregate on Region using Profit and sort to put max Profit as first row
    profit_by_region = orders_df.groupby('Region', as_index=False).agg({'Profit': 'sum'}).sort_values(by='Profit', ascending=False)
    max_region_profit = profit_by_region.iloc[0].to_dict()
    return max_region_profit

def find_most_common_ship_method(orders_df):
    "Find the most common shipping method for each Category"
    
    return 

def find_number_of_order_per_category( orders_df):
    "find the number of orders for each Category and Sub Category"

    return
