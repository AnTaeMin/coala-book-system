import pandas as pd

dict_data = {
    "mon": [1, 8, 15, 22],
    "tue": [2, 9, 6, 23],
    "wed": [3, 10, 17, 24],
    "thu": [4, 11, 18, 25],
    "fri": [5, 12, 19, 26],
    "sat": [6, 13, 20, 27],
    "sun": [7, 14, 21, 28],
}
df = pd.DataFrame(dict_data)
print(type(df))
print(df)
