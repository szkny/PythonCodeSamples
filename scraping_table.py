#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def MakeData(data,rows):
    indent = "\t"
    # 正規表現
    pattern=r'([+-]?[0-9]+\.?[0-9]*)'
    for row in rows:
        for cell in row.findAll("th"):
            tmp = re.findall(pattern,cell.get_text().strip())[0:1]
            if len(tmp):
                indent = "\t"
            else:
                indent = ""
            data += tmp + [indent]

        for cell in row.findAll("td"):
            data += re.findall(pattern,cell.get_text().strip())[0:1] + ["\n"]


outputfile = []
counter = 0
for age in range(20,70,5):
    outputfile += ["%dnenshubunpu.txt" % age]

    # URLの指定
    Age   = age - (age%10)
    url   = "http://heikinnenshu.jp/bunpu/%snenshubunpu.html" % Age
    html  = urlopen(url).read()
    bsObj = BeautifulSoup(html, "html.parser")

    # テーブルを指定
    if age%10 == 0:
        ID = 0
    else:
        ID = 1
    table = bsObj.findAll("div",{"class":"agetablebox"})[ID]
    rows  = table.findAll("tr")

    # テーブルデータ作成
    data = []
    MakeData(data, rows)

    # データ書き出し
    with open(outputfile[counter],"w") as f:
        for i in data:
            f.write(i)
    counter += 1


plot = "pyplot -w2 -L --xlabel=income\ \[10,000\ yen/month\] --ylabel=\% "
for f in outputfile:
    plot += f + " "
# plot += "&"
os.system(plot)
for f in outputfile:
    os.remove(f)

