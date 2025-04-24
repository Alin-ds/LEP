import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Pagina de unde extragem linkul
url_pagina = "https://extranet.anaf.mfinante.gov.ro/anaf/extranet/EXECUTIEBUGETARA/alte_rapoarte/alte_rapoarte2"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url_pagina, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

# 2. Caută linkul după textul ancorei
link_excel = None
for a in soup.find_all("a", href=True):
    if a.text.strip().lower().startswith("lista entitatilor publice - actualizata"):
        link_excel = a["href"]
        break

if not link_excel:
    raise Exception("❌ Nu am găsit linkul asociat cu textul 'Lista entitatilor publice - actualizata'.")

# 3. Completează linkul dacă e relativ
if not link_excel.startswith("http"):
    link_excel = "https://extranet.anaf.mfinante.gov.ro" + link_excel

print(f"✅ Link găsit: {link_excel}")

# 4. Descarcă fișierul Excel
r_excel = requests.get(link_excel)
with open("institutii.xlsx", "wb") as f:
    f.write(r_excel.content)

# 5. Convertim în JSON
df = pd.read_excel("institutii.xlsx")
df = pd.read_excel("institutii.xlsx")

# Înlocuim NaN cu șiruri goale și forțăm toate coloanele ca text
df = df.fillna("").astype(str)

# ✅ Listează coloanele care pot conține .0 și le curăță
coloane_de_curatat = [
    "CIF Entitate Publica",
    "CIF in scop TVA",
    "CIF Ordonator principal de credite (1)",
    "CIF Ordonator principal de credite (2)"
]

for col in coloane_de_curatat:
    if col in df.columns:
        df[col] = df[col].str.replace(r"\.0$", "", regex=True)

# 🔍 Debug: afișăm primele 3 valori din coloanele curățate
print("\n🔍 Preview coloane curățate:\n")
for col in coloane_de_curatat:
    if col in df.columns:
        print(f"{col}:")
        print(df[col].head(3).tolist())
        print("-" * 40)

df = df.fillna("").astype(str)
df.to_json("institutii.json", orient="records", force_ascii=False)

