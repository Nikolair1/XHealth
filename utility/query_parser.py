import csv


# Parses twitter URLS to just extract username
def parse_csv(filename):
    results = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            link = row[0]
            tokens = link.split("/")
            results.append(tokens[-1])
    return results


filename = "accounts.csv"
# print(parse_csv(filename))