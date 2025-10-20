# Order Processing Lambda
Description of project

## Project Structure
```text
DATA-ENGINEERING-ASSESSMENT
├───app
└───terraform
    ├───assignment
    └───modules
        ├───ecr-repo
        └───lambda
```
### app
Contains Python code for the Lambda Function
### terraform
Contains all terraform code, organized into `modules`.
Each module contains its own readme for reference
### base directory
Contains the following:
- Dockerfile
  - Packages Python code in `\app` using `requirements.txt`
- requirements.txt
  - List of pip package required to run Python code in `\app`
  - Used to create Docker image

## Lambda Python Code
### Inputs
Reads a CSV file from the S3 bucket: `nmd-assignment-Samantha-Eidson-input-bucket`
### Outputs
Writes 3 CSV files to the S3 bucket: `nmd-assignment-Samantha-Eidson-output-bucket`
- `most_profitable_region.csv`
  - Columns: **Region**, **Profit**
  - Only contains 1 row
  - Assumptions: In the event of more than one **Region** sharing the maximum **Profit**, only the first is selected
- `most_common_ship_mode_per_category.csv`
  - Columns: **Category**, **Ship Mode**, **Orders**
  - Contains only 1 row for each **Category**
  - Assumptions: In the event of more than one **Category**/**Ship Mode** sharing the maximum **Orders**, only the first is selected
- `orders_per_category_sub_category.csv`
  - Columns: **Category**, **Sub Category**, **Orders**
  - Contains only 1 row for each combination of **Category** and **Sub Category**
### Organization
#### lambda.py
- `lambda_handler(event, context)`
- `get_s3_path_from_event(event)`
- `get_input_data_from_s3(event)`
- `write_output_data_to_s3(data, key)`
```python
def lambda_handler(event, context)
"""
Main function that reads/writes data and calls analytics functions

Parameters
----------
event : dict
    event used to invoke Lambda function
context: LambdaContext
    provides details on the Lambda function and its invokation
"""
def get_s3_path_from_event(event)
"""
Retrieves the S3 path from the invokating event
Assumes at least the following structure
{
    'Records': [
        {
            's3': {
                'bucket': {
                    'name': str
                },
                'object': {
                    'key': str
                }
            }
        }
    ]
}

Parameters
----------
event: dict
    event used to invoke Lambda function

Returns
-------
bucket: str
    S3 bucket found in path event['Records'][0]['s3']['bucket']['name']
key: str
    S3 key found in path event['Records'][0]['s3']['object']['key']

Raises
------
KeyError
    Occurs when assumed path is in event JSON not found
"""

def get_input_data_from_s3(event)
""" 
Gets input data from file in S3 given path from input event

Parameters
----------
event: dict
    event used to invoke Lambda function

Returns
-------
data: Pandas DataFrame
    DataFrame containing data from CSV file at S3:bucket/key from event 

Raises
------
KeyError
    propagated from get_s3_path_from_event()
Exception
    Any exception caused by inability to read file from S3
"""

def write_output_data_to_s3(data, key)
""" 
description
Parameters
----------
data: Pandas DataFrame
    Data to be written to file in S3
key: str
    path within S3 bucket to write file to
    S3 bucket defined by global variable

Returns
-------
write_successfull: bool
    True if s3.put_object() function returns with a 200 response code
"""
```
#### orders_analytics.py
- Classes
  - `MissingColumns`
- Functions
  - `check_for_required_columns(columns_used, columns_available)`
  - `calculate_profit_by_order(orders_df)`
  - `calculate_most_profitable_region(orders_df)`
  - `find_most_common_ship_method(orders_df)`
  - `find_number_of_order_per_category(orders_df)`
```python
class MissingColumns(Exception)
"""
Exception to handle missing columns in DataFrames
Extends Exception
Only changes Exception message as follows: f"The following columns are not found in the DataFrame: {columns}"
"""

def check_for_required_columns(columns_used, columns_available)
""" 
Check that all required column names are found in the list of available column names

Parameters
----------
columns_used: Union[str, List[str]]
    column(s) required to be in the DataFrame for analysis to occur
columns_available: List[str]
    Columns of current DataFrame

Raises
------
MissingColumns
    If there are any columns within columns_used list that are not in columns_available, raise MissingColumns exception with the list of missing columns
"""

def calculate_profit_by_order(orders_df: pd.DataFrame) -> pd.DataFrame
""" 
Calculate profit for each order in the DataFrame

Parameters
----------
orders_df: Pandas DataFrame
    DataFrame containing order data read from S3
    Required columns: ['List Price', 'Discount Percent', 'cost price', 'Quantity']

Returns
-------
orders_df: Pandas DataFrame
    Same as input orders_df with the addition of the 'Profit' column
"""

def calculate_most_profitable_region(orders_df)
""" 
Calculate the most profitable region and its profit

Parameters
----------
orders_df: Pandas DataFrame
    DataFrame containing order data read from S3
    Required columns: 'Region'

Returns
-------
max_region_profit: Pandas DataFrame
    Single row DataFrame
    Columns: ['Region', 'Profit']
"""

def find_most_common_ship_method(orders_df)
""" 
Find the most common shipping method for each Category

Parameters
----------
orders_df: Pandas DataFrame
    DataFrame containing order data read from S3
    Required columns: ['Category', 'Ship Mode', 'Order Id']

Returns
-------
max_ship_method_category: Pandas DataFrame
    Single row for each 'Category'
    Columns: ['Category', 'Ship Mode', 'Orders']
"""

def find_number_of_order_per_category(orders_df: pd.DataFrame) -> pd.DataFrame:
""" 
Find the number of orders for each Category and Sub Category

Parameters
----------
orders_df: Pandas DataFrame
    DataFrame containing order data read from S3
    Required columns: ['Category', 'Sub Category', 'Order Id']

Returns
-------
category_subcategory_counts: Pandas DataFrame
    Single row for each combination of ['Category', 'Sub Category']
    Columns: ['Category', 'Sub Category', 'Orders']
"""
```

### Assumptions
The logic was developed under the following assumptions:
- Given multiple possible maximum values, only select the first (no ties)
  - If this is not the case, additional logic will be required
- If one ouput file fails to write, the others should still be created
  - If this is not the case, additional effort will be required to remove files created before the failure
- Input/Output files are intended to be short-lived and overwritten
  - Naming of output files is static; so, each invokation of this function will overwrite them
  - If output files are meant for medium- or long-term storage either:
    - Append current file names to input file name (minus extension)
    - Create folder in output S3 bucket for each input file
- Lambda function should not "fail" but rather have all errors written to logs
  - Depending on downstream architecture, this may be the case

## Usage
The Order Processing Lambda function is invoked via an S3 bucket notification occuring at Object Creation for any .csv file in the [input bucket](#inputs)

## Requirements
- Python 3.12
- Docker
- Terraform
- AWS CLI

## Setup
Local setup steps

## Deploy
Deployment Instructions

## Testing
Steps to Test code