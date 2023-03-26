#!/usr/bin/env python3
import csv
import sys
import xlrd
from prettytable import PrettyTable
import argparse

__version__ = "1.0"
__author__ = "Kacper Dudczak"


def get_file_type(filename):
    """
    Determine the type of a file based on its extension.

    Parameters:
    filename (str): The name of the file to check the type of.

    Returns:
    str or None: The file type as a string (csv, tsv, xls, or xlsx) if the file's extension matches one of these types. Returns None if the file's extension is not recognized.

    Examples:
    >>> get_file_type("data.csv")
    'csv'
    >>> get_file_type("report.xlsx")
    'xlsx'
    >>> get_file_type("image.jpg")
    None
    """

    if filename.endswith(".csv"):
        return "csv"
    elif filename.endswith(".tsv"):
        return "tsv"
    elif filename.endswith(".xls"):
        return "xls"
    elif filename.endswith(".xlsx"):
        return "xlsx"
    else:
        return None


def read_table_from_file_as_list_of_dicts(filename):
    """
    Reads a table from a file and returns it as a list of dictionaries.

    The file type is determined by the file's extension. Currently, the function
    supports CSV, TSV, XLS, and XLSX files.

    Parameters:
    filename (str): The name of the file to read from.

    Returns:
    list of dict: A list of dictionaries, where each dictionary represents a row
                  in the table and the keys are the column names.

    Raises:
    SystemExit: If the file's extension is not recognized.

    Examples:
    >>> read_table_from_file_as_list_of_dicts("data.csv")
    [{'name': 'Alice', 'age': '25', 'city': 'New York'},     {'name': 'Bob', 'age': '30', 'city': 'Los Angeles'}]
    >>> read_table_from_file_as_list_of_dicts("data.xlsx")
    [{'name': 'Alice', 'age': '25', 'city': 'New York'},     {'name': 'Bob', 'age': '30', 'city': 'Los Angeles'}]
    """

    file_type = get_file_type(filename)
    if file_type == "csv":
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            data = []
            for row in reader:
                data.append(row)
    elif file_type == "tsv":
        with open(filename, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            data = []
            for row in reader:
                data.append(row)
    elif file_type == "xls":
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)
        data = []
        for row in range(1, worksheet.nrows):
            data.append({
                worksheet.row_values(0)[i]: worksheet.row_values(row)[i]
                for i in range(worksheet.ncols)
            })
    elif file_type == "xlsx":
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)
        data = []
        for row in range(1, worksheet.nrows):
            data.append({
                worksheet.row_values(0)[i]: worksheet.row_values(row)[i]
                for i in range(worksheet.ncols)
            })
    else:
        print("File type not recognized")
        sys.exit(1)
    return data



def display_table_dimensions(data):
    """
    Display the dimensions of a table as a PrettyTable.

    Parameters:
    data (list of dict): A list of dictionaries representing the table, where
                         each dictionary represents a row in the table and the
                         keys are the column names.

    Returns:
    None.

    Examples:
    >>> data = [            {'name': 'Alice', 'age': 25, 'city': 'New York'},            {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}        ]
    >>> display_table_dimensions(data)
    +----------------------------+----------------+------------------+
    | Number of rows with Header | Number of rows | Number of columns|
    +----------------------------+----------------+------------------+
    |             2              |        1       |         3        |
    +----------------------------+----------------+------------------+
    """
    table = PrettyTable()
    table.field_names = ["Number of rows with Header", "Number of rows", "Number of columns"]
    table.add_row([len(data), len(data) - 1, len(data[0].keys())])
    print(table)

def display_columns_and_types(data):
    """
    Display the names and types of the columns in a table as a PrettyTable.

    Parameters:
    data (list of dict): A list of dictionaries representing the table, where
                         each dictionary represents a row in the table and the
                         keys are the column names.

    Returns:
    None.

    Examples:
    >>> data = [            {'name': 'Alice', 'age': 25, 'city': 'New York'},            {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}        ]
    >>> display_columns_and_types(data)
    +------------+----------------+
    | Column name|   Column type   |
    +------------+----------------+
    |    name    |  not_numeric    |
    |    age     |    numeric      |
    |    city    |  not_numeric    |
    +------------+----------------+

    """
    columns = data[0].keys()
    table = PrettyTable()
    table.field_names = ["Column name", "Column type"]
    for column in columns:
        column_type = check_column_type(data, column)
        table.add_row([column, column_type])
    print(table)


def check_column_type(data, column_to_check):
    """
    Determine whether a column in a table contains numeric or non-numeric data.

    Parameters:
    data (list of dict): A list of dictionaries representing the table, where
                         each dictionary represents a row in the table and the
                         keys are the column names.
    column_to_check (str): The name of the column to check.

    Returns:
    str: The type of the column, either "numeric" if all values in the column are
         numeric, or "not_numeric" if at least one value in the column is not
         numeric.

    Examples:
    >>> data = [            {'name': 'Alice', 'age': '25', 'city': 'New York'},            {'name': 'Bob', 'age': '30', 'city': 'Los Angeles'}        ]
    >>> check_column_type(data, 'name')
    'not_numeric'
    >>> check_column_type(data, 'age')
    'numeric'
    >>> check_column_type(data, 'city')
    'not_numeric'

    """
    column_data = [row[column_to_check] for row in data if row[column_to_check] != "" and row[column_to_check] != "None" and row[column_to_check] != "NaN"]
    if all(value.replace('.', '', 1).isdigit() or value.isnumeric() or value.isdecimal() for value in column_data):
        return "numeric"
    else:
        return "not_numeric"


def change_values_in_table(data, column_to_change, old_value, new_value):
    """
    Modify the values of a specific column in a table.

    Parameters:
    data (list of dicts):   The table to modify.
                            column_to_change (str): The name of the column to modify. If set to "all", every value in every column will be checked for replacement.
    old_value (str): The value to be replaced.
    new_value (str): The new value to be assigned to the old value.

    Returns:
    list of dicts: The modified table with updated values.

    Examples:
    >>> data = [{'Name': 'John', 'Age': '30', 'Money': '30'}, {'Name': 'Mary', 'Age': '-', 'Money': '-'}]
    >>> change_values_in_table(data, 'Age', '-', 'NaN')
    [{'Name': 'John', 'Age': '31', 'Money': '30'}, {'Name': 'Mary', 'Age': 'NaN', 'Money': '-'}]
    >>> change_values_in_table(data, 'all', '30', '0')
    [{'Name': 'John', 'Age': '0', 'Money': '0'}, {'Name': 'Mary', 'Age': '-', 'Money': '-}]
    """
    if column_to_change == "all":
        for row in data:
            for key in row.keys():
                if row[key] == old_value:
                    row[key] = new_value
    else:
        for row in data:
            if row[column_to_change] == old_value:
                row[column_to_change] = new_value
    return data


def replace_nan_with_mean(data):
    """
    Replace missing values in a table with the mean of the column.

    Parameters:
    data (list of dicts): The table to modify.

    Returns:
    list of dicts: The modified table with updated values.

    Raises:
    ValueError: If the column contains non-numeric values.
    
    Example:
    >>> data = [{'Name': 'John', 'Age': '30', 'Money': '30'}, {'Name': 'Mary', 'Age': 'NaN', 'Money': 'NaN'}]
    >>> replace_nan_with_mean(data)
    [{'Name': 'John', 'Age': '30', 'Money': '30'}, {'Name': 'Mary', 'Age': '30', 'Money': '30'}]
    """
    columns = data[0].keys()
    for key in columns:
        column_data = [row[key] for row in data if row[key] != "" and row[key] is not None and row[key] != "NaN"]
        if all(value.isdigit() for value in column_data):
            column_data = [int(value) for value in column_data]
            mean = sum(column_data) / len(column_data)
            for row in data:
                if row[key] == "" or row[key] == "None" or row[key] == "NaN":
                    row[key] = str(mean)
        else:
            most_common_value = max(set(column_data), key=column_data.count)
            for row in data:
                if row[key] == "" or row[key] == "None" or row[key] == "NaN":
                    row[key] = most_common_value
    return data



def save_list_of_dicts_to_file(data, filename):
    """
    Save a list of dictionaries to a file.

    Parameters:
    data (list of dicts): The data to save.
    filename (str): The name of the file to save the data to.

    Returns:
    None

    Examples:
    >>> data = [{'Name': 'John', 'Age': '30', 'Money': '30'}, {'Name': 'Mary', 'Age': '31', 'Money': '0'}]
    >>> save_list_of_dicts_to_file(data, 'test.csv')
    >>> save_list_of_dicts_to_file(data, 'test.tsv')
    >>> save_list_of_dicts_to_file(data, 'test.xls')
    """
    file_type = get_file_type(filename)
    if file_type == "csv":
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    elif file_type == "tsv":
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(data)
    elif file_type == "xls":
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)
        for row in range(1, worksheet.nrows):
            for i in range(worksheet.ncols):
                worksheet.write(row, i, data[row-1][worksheet.row_values(0)[i]])
    elif file_type == "xlsx":
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)
        for row in range(1, worksheet.nrows):
            for i in range(worksheet.ncols):
                worksheet.write(row, i, data[row-1][worksheet.row_values(0)[i]])
    else:
        print("File type not recognized")
        sys.exit(1)


def display_table_as_pretty_table(data):
    """
    Display a table as a pretty table.

    Parameters:
    data (list of dicts): The table to display.

    Returns:
    None

    Examples:
    >>> data = [{'Name': 'John', 'Age': '30', 'Money': '30'}, {'Name': 'Mary', 'Age': '31', 'Money': '0'}]
    >>> display_table_as_pretty_table(data)
    +------+-----+-------+
    | Name | Age | Money |
    +------+-----+-------+
    | John |  30 |    30 |
    | Mary |  31 |     0 |
    +------+-----+-------+
    """
    table = PrettyTable(data[0].keys())
    for row in data:
        table.add_row(row.values())
    print(table)


def parse_args():
    """
    Parse command line arguments.

    Parameters:
    none

    Returns:
    argparse.Namespace: The parsed arguments.

    Examples:
    >>> args = parse_args()
    >>> args.filename
    'test.csv'
    """
    desc = f"Simple table manipulator. Version {__version__} by {__author__}"
    parser = argparse.ArgumentParser(description=desc)
    # required arguments
    parser.add_argument("filename", help="path to the input file")

    # optional arguments
    parser.add_argument("-o", "--output", help="path to the output file")
    parser.add_argument("-c", "--change", nargs=3, metavar=("column", "old", "new"), help="change values in the column")
    parser.add_argument("-n", "--nan", action="store_true", help="replace NaN or empty places with mean value")
    parser.add_argument("-d", "--dimensions", action="store_true", help="display table dimensions")
    parser.add_argument("-l", "--list-columns", action="store_true", help="display list of columns in the table")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    data = read_table_from_file_as_list_of_dicts(args.filename)


    if args.output:
        type = get_file_type(args.filename)
        name = args.output
        save = name + "." + type
        save_list_of_dicts_to_file(data, save)
    if args.change:
        data = change_values_in_table(data, args.change[0], args.change[1], args.change[2])
    if args.nan:
        data = replace_nan_with_mean(data)
    if args.dimensions:
        display_table_dimensions(data)
    if args.list_columns:
        display_columns_and_types(data)
    else:
        display_table_as_pretty_table(data)


#I'm not sure if this is the best way to do it, but it works. I'm open to suggestions. Thanks for reading.
