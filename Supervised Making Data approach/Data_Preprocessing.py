# //////////  Check the folder in directory


# This give the combined json file of all tables

import json
import os
import pandas as pd

filepaths = ["ecom_tables_and_columns_new_with_dimensions/","metrics_table_new/"]



def parse_json_files_in_folders(folder_paths):
    json_data = []

    for folder_path in folder_paths:
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    json_data.append(data)

    return json_data

json_data = parse_json_files_in_folders(filepaths)


# Now i converting the json file into csv

# Helper function to convert columns to a compact JSON style string
def columns_to_string(columns):
    column_strings = []
    for col in columns:
        col_str = json.dumps(col)
        column_strings.append(col_str)
    return "[" + ", ".join(column_strings) + "]"


rows = []
for table in json_data:
    description = table.get("description", "")
    primary_key_columns = ", ".join(table.get("primary_key_column", []))
    columns_details = columns_to_string(table.get("columns", []))

    combined_description = (f"Description: {description}\n"
                            f"Primary Key Columns: {primary_key_columns}\n"
                            f"Columns: {columns_details}")

    row = {
        "name": table.get("name", ""),
        "description": description,
        "primary_key_columns": primary_key_columns,
        "columns": columns_details,
        "combined_description": combined_description
    }
    rows.append(row)

# Create DataFrame
df1 = pd.DataFrame(rows, columns=['name', 'description', 'primary_key_columns', 'columns', 'combined_description'])


# Converting relation.json into Csv

# Load JSON data from a file
with open('/content/relationships_minimized.json', 'r') as file:
    data = json.load(file)

# Prepare the data for the DataFrame
rows = []
for from_table_name, links in data.items():
    for link in links:
        from_table = link.get("FromTable", "")
        from_columns = ", ".join(link.get("FromColumn", []))
        to_table = link.get("ToTable", "")
        to_columns = ", ".join(link.get("ToColumn", []))

        combined_description = json.dumps(link)

        row = {
            "from_table_name": from_table_name,
            "from_table": from_table,
            "from_columns": from_columns,
            "to_table": to_table,
            "to_columns": to_columns,
            "combined": combined_description
        }
        rows.append(row)

# Create DataFrame
df2 = pd.DataFrame(rows, columns=['from_table_name', 'from_table', 'from_columns', 'to_table', 'to_columns', 'combined'])



# Preprocessing

df1 = df1.drop(columns=['description', 'primary_key_columns', 'columns'])
df2 = df2.drop(columns=['from_table', 'from_columns', 'to_table', 'to_columns'])



# Define the new column names
new_column_names = {
    'name': 'Table Name',
    'combined_description': 'Information About Table/Relationship',
}

# Rename the columns
df1.rename(columns=new_column_names, inplace=True)

new_column_names = {
    'from_table_name': 'Table Name',
    'combined': 'Information About Table/Relationship',
}
df2.rename(columns=new_column_names, inplace=True)


# Combine the DataFrames
combined_df = pd.concat([df1, df2])


# Reset the index
combined_df.reset_index(drop=True, inplace=True)



# /////////////////////////////////// Making this as supervised Finetuning dataset ///////////////////

df = combined_df
# Merge the columns 'col1' and 'col2' into a new column 'input'
df['input'] = df['Table Name'].astype(str) + ' :  ' + df['Information About Table/Relationship'].astype(str)

df = df.drop(['Table Name', 'Information About Table/Relationship'],axis=1)


# Define the new column value
instruction_value = "Input column contains everything about the table and their relationship with other tables and you have to learn all information about the Database.So that when thier is questin you take help from this information and give answer in expected output format"

# Add the new column to the DataFrame
df['instruction'] = instruction_value

output_value = "Yes i learned about the Database and Relationship"
df['output']= output_value

df.to_csv("fine_tune_data.csv",index=False)

