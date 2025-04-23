import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 1. Pagina cu linkurile către fișierele Excel
pagina_url = "https://extranet.anaf.mfinante.gov.ro/anaf/extranet/EXECUTIEBUGETARA/alte_rapoarte/alte_rapoarte2"

# 2. Citește HTML-ul paginii
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(pagina_url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

# 3. Caută primul link care conține .xls sau .xlsx
link_excel = None
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.endswith(".xls") or href.endswith(".xlsx"):
        if not href.startswith("http"):
            href = "https://extranet.anaf.mfinante.gov.ro" + href
        link_excel = href
        break

if not link_excel:
    raise Exception("Nu am găsit linkul către fișierul Excel!")

print(f"📁 Link găsit: {link_excel}")

# 4. Descarcă fișierul Excel
r_excel = requests.get(link_excel)
with open("institutii.xlsx", "wb") as f:
    f.write(r_excel.content)

# 5. Încarcă Excelul în Pandas și convertește în JSON
df = pd.read_excel("institutii.xlsx")

# 🔧 (opțional) Selectează doar coloanele relevante
# df = df[["Denumire", "Cod fiscal", "Județ", "Tip instituție"]]

# Înlocuiește NaN cu șiruri goale și asigură-te că toate coloanele sunt string
df = df.fillna("").astype(str)

# Salvează ca JSON
df.to_json("institutii.json", orient="records", force_ascii=False)

print("✅ institutii.json generat cu succes.")
