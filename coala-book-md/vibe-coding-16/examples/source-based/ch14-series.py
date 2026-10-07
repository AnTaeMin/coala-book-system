import pandas as pd

ser = pd.Series({"one": 1, "two": 2, "three": 3})
print(ser.to_dict())
print(ser.index.tolist())
print(ser.values.tolist())
