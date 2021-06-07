import pandas as pd
charlie = pd.Series([1,2,3,4])
tessa = pd.Series([1,2,3,4])
df = pd.DataFrame([charlie,tessa])
print(df)
print(df.tail(21))