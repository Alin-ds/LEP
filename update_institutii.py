import requests
import re
import pandas as pd

# 1. Pagina unde apare fișierul
url_pagina = "https://extranet.anaf.mfinante.gov.ro/anaf/extranet/EXECUTIEBUGETARA/alte_rapoarte/alte_rapoarte2"
r = requests.get(url_pagina, headers={"User-Agent": "Mozilla/5.0"})
html = r.text

# 2. Caută denumirea fișierului Excel
match = re.search(r'Lista_EP_portal_\d{2}\.\d{2}\.\d{4}\.xls', html)
if not match:
    raise Exception("❌ Nu am găsit fișierul Excel în textul paginii.")

fisier = match.group(0)
print(f"✅ Fișier găsit: {fisier}")

# 3. Construim linkul complet
link_excel = f"https://extranet.anaf.mfinante.gov.ro/anaf/extranet/EXECUTIEBUGETARA/alte_rapoarte/alte_rapoarte2/{fisier}"
print(f"🔗 Link complet: {link_excel}")

# 4. Descarcă fișierul Excel
r_excel = requests.get(link_excel)
with open("institutii.xlsx", "wb") as f:
    f.write(r_excel.content)

# 5. Transformă în JSON
df = pd.read_excel("institutii.xlsx")
df = df.fillna("").astype(str)
df.to_json("institutii.json", orient="records", force_ascii=False)

print("✅ institutii.json generat cu succes.")
