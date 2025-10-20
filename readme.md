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
Features of code input/outputs

## Usage
How the Lambda function is invoked

## Requirements
Install requirements

## Setup
Local setup steps

## Deploy
Deployment Instructions

## Testing
Steps to Test code