import pandas as pd
import csv
with open("output.txt") as f:
    lines = f.read()
    first = lines.split("\n", 1)[0]
z = first.split(",")

dict = {'url': z}
df = pd.DataFrame(dict)

df.to_csv("x.csv")
