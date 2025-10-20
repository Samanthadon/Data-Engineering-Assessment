import sys
import json
import os
import io
import boto3
import pandas as pd
from typing import Tuple

import orders_analytics

"""
Modify this lambda function to perform the following questions

Done - 1. Find the most profitable Region, and its profit
2. What shipping method is most common for each Category
3. Output a glue table containing the number of orders for each Category and Sub Category
"""

s3 = boto3.client('s3')

def get_s3_path_from_event(event : dict) -> Tuple[str, str]:
    """Returns the S3 path from the lambda event record"""
    try:
        record_s3 = event['Records'][0]['s3']
        input_bucket = record_s3['bucket']['name']
        input_key = record_s3['object']['key']
    except KeyError as ke:
        print("Unable to read input S3 bucket/key from Lambda Event")
        raise ke
    else:
        return (input_bucket, input_key)

def get_input_data_from_s3(event: dict) -> pd.DataFrame:
    try:
        input_s3_bucket, input_s3_key = get_s3_path_from_event(event)
        file_obj = s3.get_object(Bucket=input_s3_bucket, Key=input_s3_key)
        input_df = pd.read_csv(io.BytesIO(file_obj['Body'].read()))
    except KeyError as ke:
        # KeyError caused by get_s3_path_from_event() already handled and should be propagated 
        raise ke
    except Exception as e:
        print(f'Unable to read input file from S3 path: {input_s3_bucket}/{input_s3_key}')
        raise e
    else:
        return input_df


def lambda_handler(event, context):
    """Lambda function to process S3 events and perform analytics on orders data"""
    try:
        # Read CSV from S3
        orders = get_input_data_from_s3(event)
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


