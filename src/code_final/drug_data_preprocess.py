import pandas as pd

df = pd.read_excel("data/drug_all_information.xlsx")

for col in df.columns:
    print(col)

df_final = pd.DataFrame()
df_final["title"] = df["Бүтээгдэхүүний нэр apteka"]
df_final["text"] = df["Катологи"] + " " + "Үнэ: " + df["Үнэ"].astype("str") + " Тайлбар: " + df["Товч тайлбар"] + " " + df["Үзүүлэлтүүд"]  + " " + df["Дэлгэрэнгүй тайлбар"]
df_final["source"] = df["Бүтээгдэхүүний нэр apteka"]

df_final.to_excel("data/drug.xlsx", index=False)