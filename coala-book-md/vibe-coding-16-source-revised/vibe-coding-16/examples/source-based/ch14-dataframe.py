import pandas as pd

df = pd.DataFrame(
    [[15, "여", "중2"], [17, "남", "고1"]],
    index=["현아", "태민"],
    columns=["나이", "성별", "학년"],
)
print(df.index.tolist())
print(df.columns.tolist())
print(df.loc["태민"].to_dict())
