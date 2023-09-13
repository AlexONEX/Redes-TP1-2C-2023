#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import os

directorio = "muestras01"
muestras = pd.DataFrame({})
for filename in os.listdir(directorio):
    f = os.path.join(directorio, filename)
    print(f)
    temp = pd.read_csv(f)
    muestras = pd.concat([muestras, temp], axis = 0, ignore_index = True)
print(muestras.columns)
print(muestras)

fig = sns.barplot(data = muestras, x = "protocolo", y = "cantidad", hue = "tipo_destino")
f = fig.get_figure()
f.savefig("plot.pdf")
        