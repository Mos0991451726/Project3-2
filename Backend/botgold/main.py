import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from download import download_all
from cleaners.clean_gdp       import clean_gdp
from cleaners.clean_inflation import clean_inflation
from cleaners.clean_gold      import clean_gold
from cleaners.clean_xau       import clean_xau
from cleaners.clean_wiki      import clean_wiki
from scrapers.scrape_wiki     import scrape_all

print("=" * 50)
print("Step 1: Download datasets from Kaggle")
print("=" * 50)
download_all()

print("\n" + "=" * 50)
print("Step 2: Clean datasets")
print("=" * 50)
df_gdp       = clean_gdp()
df_inflation = clean_inflation()
df_gold      = clean_gold()
df_xau       = clean_xau()

print("\n" + "=" * 50)
print("Step 3: Scrape Wikipedia")
print("=" * 50)
scrape_all()

print("\n" + "=" * 50)
print("Step 4: Clean Wikipedia text")
print("=" * 50)
clean_wiki()

print("\n✅ All done! ต่อไปรัน: python embedder/embed.py")
