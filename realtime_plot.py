# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:21:22 2026

@author: Majdo
"""
# -*- coding: utf-8 -*-
import pyqtgraph as pg
from PyQt5 import QtWidgets
import numpy as np

class LivePlot:
    def __init__(self):
        self.app = pg.mkQApp()

        # Fenêtre
        self.window = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()
        self.window.setLayout(self.layout)

        # Sélecteur de signal
        self.selector = QtWidgets.QComboBox()
        self.selector.addItems(["Température", "Humidité", "Luminosité"])
        self.layout.addWidget(self.selector)

        # Graphe
        self.plot = pg.PlotWidget(title="Données capteurs")
        self.layout.addWidget(self.plot)

        # Label stats
        self.stats_label = QtWidgets.QLabel("Stats:")
        self.layout.addWidget(self.stats_label)

        # Données
        self.timestamps = []
        self.temp = []
        self.hum = []
        self.lum = []

        # Courbe
        self.curve = self.plot.plot(pen='y')

        # Textes (créés UNE seule fois)
        self.min_text = pg.TextItem(anchor=(0, 1))
        self.max_text = pg.TextItem(anchor=(0, 1))
        self.mean_text = pg.TextItem(anchor=(0, 1))

        self.plot.addItem(self.min_text)
        self.plot.addItem(self.max_text)
        self.plot.addItem(self.mean_text)

        # Labels axes
        self.plot.setLabel('left', 'Valeur')
        self.plot.setLabel('bottom', 'Mesures')

        self.window.show()

    def update(self, timestamp, temp, hum, lum):
        # Stockage
        self.timestamps.append(timestamp)
        self.temp.append(temp)
        self.hum.append(hum)
        self.lum.append(lum)

        # Choix utilisateur
        choice = self.selector.currentText()

        if choice == "Température":
            data = self.temp
            name = "Température (°C)"
        elif choice == "Humidité":
            data = self.hum
            name = "Humidité (%)"
        else:
            data = self.lum
            name = "Luminosité (%)"

        # Axe X
        x = list(range(len(data)))

        # Update courbe
        self.curve.setData(x, data)
        self.plot.setTitle(name)

        # Stats
        if len(data) > 0:
            arr = np.array(data)
            min_val = arr.min()
            max_val = arr.max()
            mean_val = arr.mean()

            # Label texte
            self.stats_label.setText(
                f"{name} | Min: {min_val:.2f} | Max: {max_val:.2f} | Moy: {mean_val:.2f}"
            )

            # Position des textes (à droite du graphe)
            xpos = len(data)

            self.min_text.setText(f"Min: {min_val:.1f}")
            self.min_text.setPos(xpos, min_val)

            self.max_text.setText(f"Max: {max_val:.1f}")
            self.max_text.setPos(xpos, max_val)

            self.mean_text.setText(f"Moy: {mean_val:.1f}")
            self.mean_text.setPos(xpos, mean_val)

    def run(self):
        pg.exec()






# class LivePlot:
#     def __init__(self):
#         self.app = pg.mkQApp()

#         self.window = QtWidgets.QWidget()
#         self.layout = QtWidgets.QVBoxLayout()
#         self.window.setLayout(self.layout)

#         self.plot = pg.PlotWidget(title="Données capteurs")
#         self.layout.addWidget(self.plot)

#         # Données
#         self.x = []
#         self.temp = []
#         self.hum = []
#         self.lum = []

#         # Courbes
#         self.curve_temp = self.plot.plot(self.temp, pen='r', name="Temp")
#         self.curve_hum = self.plot.plot(self.hum, pen='b', name="Hum")
#         self.curve_lum = self.plot.plot(self.lum, pen='g', name="Lum")

#         self.plot.addLegend()
#         self.plot.setLabel('left', 'Valeurs')
#         self.plot.setLabel('bottom', 'Mesures')

#         self.window.show()

#     def update(self, timestamp, temp, hum, lum):
#         self.x.append(len(self.x))

#         self.temp.append(temp)
#         self.hum.append(hum)
#         self.lum.append(lum)

#         self.curve_temp.setData(self.x, self.temp)
#         self.curve_hum.setData(self.x, self.hum)
#         self.curve_lum.setData(self.x, self.lum)

#     def run(self):
#         pg.exec()
        
        
