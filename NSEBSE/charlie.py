import csv

with open("symbols.csv") as file:
    reader = csv.reader(file)
    for line in reader:
       
        for token in line:
            if(token == ""):
                print("empty token")
