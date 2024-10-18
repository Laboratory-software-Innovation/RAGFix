import pandas as pd
import json

def create_errors_json(csv_file_path, json_file_path):
    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Filter rows where there is an exception
    exceptions_df = df[df['exception_type'].notnull() & df['exception_type'].str.strip().astype(bool)]

    # Extract the examples and convert them to JSON format
    exceptions_list = []
    for index, row in exceptions_df.iterrows():
        try:
            example = eval(row['example'])  # Convert the string representation to a dictionary
            exceptions_list.append(example)
        except Exception as e:
            print(f"Failed to process row {index}: {e}")

    # Save the exceptions to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(exceptions_list, json_file, indent=4)

# Define file paths
csv_file_path = 'exp10.csv'  # Update this path
json_file_path = 'errors2.json'     # Update this path

# Create errors.json
create_errors_json(csv_file_path, json_file_path)
