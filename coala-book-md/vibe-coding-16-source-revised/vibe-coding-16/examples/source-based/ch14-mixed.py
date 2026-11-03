import pandas as pd

values = ["2022-01-01", 2.14, "song", 1000, True]
sr = pd.Series(values)
print(sr.index.tolist())
print(sr.values.tolist())
