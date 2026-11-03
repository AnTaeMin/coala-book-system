import pandas as pd

list_data = ["2022-01-01", 2.14, "song", 1000, True]
sr = pd.Series(list_data)
print(sr)
print(sr.index)
print(sr.values)
