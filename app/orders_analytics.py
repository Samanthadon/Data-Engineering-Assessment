import pandas as pd
"Complete thes functions or write your own to perform the following tasks"

def calculate_profit_by_order(orders_df: pd.DataFrame) -> pd.DataFrame:
    "Calculate profit for each order in the DataFrame"
    orders_df['Profit'] = orders_df.apply(
        lambda x: round((x['List Price'] * (1.0 - x['Discount Percent'] / 100.0) - x['cost price']) * x['Quantity'], 2),
        axis=1
    )
    return orders_df

def calculate_most_profitable_region(orders_df: pd.DataFrame) -> pd.DataFrame:
    "Calculate the most profitable region and its profit"
    # Determine the Profit/Order
    orders_df = calculate_profit_by_order(orders_df)
    # Aggregate on Region using Profit and sort to put max Profit as first row
    profit_by_region = orders_df.groupby('Region', as_index=False).agg({'Profit': 'sum'}).sort_values(by='Profit', ascending=False)
    # Note: This will only return 1 row. If there is a "tie" only the first row will be returned
    max_region_profit = profit_by_region.loc[[0]]
    return max_region_profit

def find_most_common_ship_method(orders_df: pd.DataFrame) -> pd.DataFrame:
    "Find the most common shipping method for each Category"
    # Aggregate count of orders on Category, Ship Mode
    ship_mode_counts = orders_df.groupby(['Category','Ship Mode'], as_index=False).agg(
            Order_count=('Order Id', 'count')
        )
    # Utilize groupby() to get id of max Order_count for each Category
    # Note: This will only return 1 row per category. if there is a "tie" the first listed row is selected
    max_ship_method_category = ship_mode_counts.loc[
            ship_mode_counts.groupby('Category')['Order_count'].idxmax()
        ].reset_index(drop=True)
    return max_ship_method_category

def find_number_of_order_per_category(orders_df: pd.DataFrame) -> pd.DataFrame:
    "find the number of orders for each Category and Sub Category"
    # Aggregate count of orders over Category and Sub Category
    category_subcategory_counts = orders_df.groupby(['Category', 'Sub Category'], as_index=False).agg(
            Orders=('Order Id', 'count')
        )
    return category_subcategory_counts
