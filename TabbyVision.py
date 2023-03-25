import sys
import csv
from blessings import Terminal

# funkcja wyświetlająca dane w formacie tabeli
def display_table(data):
    t = Terminal()
    table_format = "{:<15} {:<15} {:<10}"
    print(t.bold(table_format.format(*data[0])))
    print(t.bold("-" * 40))
    for row in data[1:]:
        print(table_format.format(*row))

# funkcja rozpoznająca typ pliku na podstawie rozszerzenia
def get_file_type(filename):
    if filename.endswith(".csv"):
        return "csv"
    elif filename.endswith(".tsv"):
        return "tsv"
    else:
        return None

# główna część programu
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Podaj nazwę pliku jako pierwszy argument programu.")
        sys.exit(1)

    filename = sys.argv[1]
    file_type = get_file_type(filename)

    if file_type is None:
        print("Nieznany typ pliku. Obsługiwane rozszerzenia to .csv i .tsv.")
        sys.exit(1)

    with open(filename, newline='') as f:
        if file_type == "csv":
            data = list(csv.reader(f))
        elif file_type == "tsv":
            data = list(csv.reader(f, delimiter='\t'))

    display_table(data)
