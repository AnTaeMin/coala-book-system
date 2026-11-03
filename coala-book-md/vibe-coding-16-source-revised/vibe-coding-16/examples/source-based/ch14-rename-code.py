import pandas as pd

df = pd.DataFrame(
    [[15, "여", "중2"], [17, "남", "고1"]],
    index=["현아", "태민"],
    columns=["나이", "성별", "학년"],
)
df.index = ["학생1", "학생2"]
df.columns = ["연령", "남녀", "학년"]
print(df.index.tolist())
print(df.columns.tolist())
print(df.iloc[0].to_dict())
