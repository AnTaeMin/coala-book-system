import pandas as pd

df = pd.DataFrame(
    [[15, "여", "중2"], [17, "남", "고1"]],
    index=["현아", "태민"],
    columns=["나이", "성별", "학년"],
)
print(df)
print(df.index)
print(df.columns)
