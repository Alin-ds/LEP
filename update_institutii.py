import requests
import re
import pandas as pd

# Pagina cu fișierul Excel
url = "https://extranet.anaf.mfinante.gov.ro/anaf/extranet/EXECUTIEBUGETARA/alte_rapoarte/alte_rapoarte2"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers)
html = r.text

# Caută linkul către fișierul Excel
matches = re.findall(r'href="([^"]+\.(?:xls|xlsx))"', html)
if not matches:
    raise Exception("❌ Nu am găsit niciun link către un fișier Excel în pagină.")

# Ia primul link găsit
link_excel = matches[0]
if not link_excel.startswith("http"):
    link_excel = "https://extranet.anaf.mfinante.gov.ro" + link_excel

print(f"✅ Link Excel găsit: {link_excel}")

# Descarcă fișierul Excel
response = requests.get(link_excel)
with open("institutii.xlsx", "wb") as f:
    f.write(response.content)

# Citește Excelul și salvează JSON
df = pd.read_excel("institutii.xlsx")
df = df.fillna("").astype(str)
df.to_json("institutii.json", orient="records", force_ascii=False)

print("✅ Fișier institutii.json a fost generat cu succes.")
