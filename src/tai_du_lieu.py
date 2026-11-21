# -*- coding: utf-8 -*-
"""
Tai bo du lieu MovieLens ml-latest-small ve thu muc data/.
Du lieu thuoc GroupLens, khong dua len GitHub (giay phep cua GroupLens khong cho phep phan phoi lai).
Cach chay:  py src/tai_du_lieu.py
"""
import os, urllib.request, zipfile

URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
os.makedirs("data", exist_ok=True)
tep = os.path.join("data", "ml-latest-small.zip")
print("Dang tai:", URL)
urllib.request.urlretrieve(URL, tep)
with zipfile.ZipFile(tep) as z:
    z.extractall("data")
os.remove(tep)
print("Hoan thanh! Du lieu nam trong data/ml-latest-small")
