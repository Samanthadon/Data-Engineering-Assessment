import sys
import json
import os
import pandas as pd

import orders_analytics

"""
Modify this lambda function to perform the following questions

Done - 1. Find the most profitable Region, and its profit
2. What shipping method is most common for each Category
3. Output a glue table containing the number of orders for each Category and Sub Category
"""


def get_s3_path_from_event(event : dict) -> str:
    """Returns the S3 path from the lambda event record"""
    # TODO: correct to get actual S3 path not static local path
    # Temporarily read local CSV for the sake of code development
    return "./sample_orders.csv"

def lambda_handler(event, context):
    """Lambda function to process S3 events and perform analytics on orders data"""
    try:
        # Read CSV from S3
        s3_path = get_s3_path_from_event(event)
        # TODO: read from S3 using Boto3 rather than local
        orders = pd.read_csv(s3_path)
        # Generate analytics report data
        most_profitiable_region = orders_analytics.calculate_most_profitable_region(orders)
        most_common_ship_mode =  orders_analytics.find_most_common_ship_method(orders)
        orders_per_category_subcategory = orders_analytics.find_number_of_order_per_category(orders)
        # Write CSV to S3
        # TODO: write to s3 rather than local
        most_profitiable_region.to_csv('most_profitable_region.csv', index=False)
        most_common_ship_mode.to_csv('most_common_ship_mode_per_category.csv', index=False)
        orders_per_category_subcategory.to_csv('orders_per_category_sub_category.csv', index=False)

    except FileNotFoundError as fe:
        print(f"No file found at {fe.filename}")
    except orders_analytics.MissingColumns as mc:
        print(f"Input Data missing critical columns. {mc.message}")
    except Exception as e:
        print(e.message)

lambda_handler({},"")


