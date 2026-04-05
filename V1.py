#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 14:58:56 2026

@author: elhadj
"""
import pyqtgraph as pg
import pandas as pd
from pyqtgraph.Qt import QtGui, QtWidgets, mkQApp

fichier_entree = '09021802.TXT'

# %%
df = pd.read_csv(fichier_entree,sep='\s+',header=0)
print(df)
# %%
df2 = df.drop(df[(df["Temp"]==0) & (df["Lum"] == 0 ) & (df["Hum"]== 0)].index).reset_index()
df3 = df2
df3['Time']=df2['Time'].dt.tz_localize(tz='Europe/Paris')
df3['Time_unix']=pd.to_datetime(df3['Time']).astype(int) / 10**9
# %%
app = pg.mkQApp()
win = pg.GraphicsLayoutWidget(show=True, title='Données')
win.resize(900,480)
win.setWindowTitle('Capteurs')
p1 = win.addPlot(title="Temperature",axisItems = {'bottom': pg.DateAxisItem()})
p1.showGrid(x=True, y=True)
p1.plot(df3['Time_unix'], df3['Temp'])

p2 = win.addPlot(title="Humidité",axisItems = {'bottom': pg.DateAxisItem()})
p2.showGrid(x=True, y=True)
p2.plot(df3['Time_unix'], df3['Hum'])

p3 = win.addPlot(title="Luminosité",axisItems = {'bottom': pg.DateAxisItem()})
p3.showGrid(x=True, y=True)
p3.plot(df3['Time_unix'], df3['Lum'])
# %%

if __name__ == '__main__':
    pg.exec()
