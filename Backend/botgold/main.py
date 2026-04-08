import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from download import download_all
from cleaners.clean_gdp import clean_gdp
from cleaners.clean_inflation import clean_inflation
from cleaners.clean_gold import clean_gold
from cleaners.clean_xau import clean_xau

# โหลดข้อมูล
download_all()

# Clean แต่ละ dataset
df_gdp       = clean_gdp()
df_inflation = clean_inflation()
df_gold      = clean_gold()
df_xau       = clean_xau()

print("\nAll done!")