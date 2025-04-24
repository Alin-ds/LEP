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
# Citim Excelul
df = pd.read_excel("institutii.xlsx")

# Normalizează numele coloanelor
df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

# Convertim totul în string pentru siguranță
df = df.fillna("").astype(str)

# ✅ Detectăm automat coloanele cu valori care se termină în .0
coloane_de_curatat = []
for col in df.columns:
    if df[col].str.endswith(".0").any():
        coloane_de_curatat.append(col)

# ✅ Funcție robustă pentru eliminat sufixul .0
def curata_cif(val):
    val_str = str(val).strip()
    return val_str[:-2] if val_str.endswith(".0") else val_str

# Aplicăm curățarea pe coloanele detectate
for col in coloane_de_curatat:
    df[col] = df[col].apply(curata_cif)

# 🔍 Debug: afișăm coloanele curățate + câteva valori
print("\n🧼 Coloane curățate automat:")
for col in coloane_de_curatat:
    print(f"{col}: {df[col].head(3).tolist()}")
    print("-" * 40)

# Convertim în JSON
df.to_json("institutii.json", orient="records", force_ascii=False)


