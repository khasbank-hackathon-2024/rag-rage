from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import CSVLoader
from openai import OpenAI
import pandas as pd
import numpy as np
from tqdm import tqdm

import fitz

openai_key = "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"


def get_embedding(df_docs, embedding_model):
    client = OpenAI(api_key=openai_key)
    embeds = []
    for i, row in tqdm(df_docs.iterrows(), total=df_docs.shape[0]):
        try:
            emb = client.embeddings.create(input=[" ".join(row["text"].split())], model=embedding_model).data[
                0].embedding
            embeds.append(emb)
        except:
            embeds.append(np.nan)

    df_docs['embeds'] = embeds
    df_docs = df_docs.loc[~df_docs["embeds"].isna()].reset_index(drop=True)

    return df_docs


if __name__ == "__main__":


    df = pd.read_csv("data/citypharm_data.csv")
    df["source"] = df["Link"]
    df["title"] = df["Product Name"]
    df["Price"] = df["Price"].astype("int")
    df["text"] = (df["Product Name"].astype("str") +
                  " Price: " + df["Price"].astype("str") +
                  " Category: " + df["Categories"].astype("str") +
                  " How to use: " + df["Хэрэглэх заалт"].astype("str"))
    df["length"] = df.text.apply(lambda x: len(str(x)))
    df = df.loc[df["length"] > 10].reset_index(drop=True)

    df = get_embedding(df, embedding_model="text-embedding-ada-002")
    df.to_parquet("data/df_emb_em.pkl")

    exit()


    # hospital information #
    df_hospital = pd.read_excel("data/df_hospital.xlsx")
    df_hospital["text"] = df_hospital["text"].apply(lambda txt: " эмнэлэг, ".join(str(txt).split(",")))
    df_hospital["text"] = df_hospital["text"] + " эмнэлэг"
    df_hospital["text"] = df_hospital["title"] + ": " + df_hospital["text"]

    ## eclinic blogs ###
    df_eclinic = pd.read_excel("data/df_eclinic.xlsx")
    df_eclinic["length"] = df_eclinic.text.apply(lambda x: len(str(x)))
    df_eclinic = df_eclinic.loc[df_eclinic["length"] > 10].reset_index(drop=True)

    # # monthly statistic report from health development center
    pdf_path = 'data/Emiin__medeelel__setguuli.pdf'
    pdf_document = fitz.open(pdf_path)

    num_pages = pdf_document.page_count
    df_stat_info = {"title": [], "text": [], "source": []}
    for page_number in range(num_pages):  # info text in these pages
        page = pdf_document.load_page(page_number)
        text = page.get_text()
        if len(text.split()) > 1:
            df_stat_info["title"].append("Эмийн мэдээлэл")
            df_stat_info["text"].append(" ".join(text.split()))
            df_stat_info["source"].append("https://mmra.gov.mn/Files/Emiin__medeelel__setguuli.pdf")
    pdf_document.close()
    df_stat_info = pd.DataFrame.from_dict(df_stat_info)
    df_drug = pd.read_excel("data/drug.xlsx")
    cols = ["title", "text", "source"]
    df = pd.concat([df_eclinic[cols],
                    df_hospital[cols],
                    df_stat_info[cols],
                   df_drug[cols]],
                   axis=0).reset_index(drop=True)

    df = get_embedding(df, embedding_model="text-embedding-3-large")
    df.to_parquet("data/df_emb.pkl")




