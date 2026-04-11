# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:21:22 2026

@author: Majdo
"""
from PySide6.QtWidgets import QApplication, QVBoxLayout,QComboBox,QLabel
from PySide6.QtCore import QThread,Signal,Slot
import pyqtgraph as pg
import numpy as np
import time

class MainWindow(pg.GraphicsLayoutWidget):

    def __init__(self,GraphWindow):
        super().__init__(parent=None)
        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle('Capteur')
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Sélecteur de signal
        self.selector = QComboBox()
        self.selector.addItems(["Température", "Humidité", "Luminosité"])
        layout.addWidget(self.selector)
        self.choice = self.selector.currentText()
        self.selector.currentTextChanged.connect(self.choice_changed)

        #Sélecteur de mode
        self.modes = QComboBox()
        self.modes.addItems(["Simulation","Réél"])
        layout.addWidget(self.modes)        
        self.mode = self.modes.currentText()
        self.modes.currentTextChanged.connect(self.mode_changed)

        self.plotwidget = GraphWindow(self.choice, self.mode)
        layout.addWidget(self.plotwidget)

        #Label stats
        self.stats_label = QLabel("Stats:")
        layout.addWidget(self.stats_label)

    def choice_changed(self,s):
        self.plotwidget.update_choice(s)

            
    def mode_changed(self,s):

        self.plotwidget.update_mode(s)
    def closeEvent(self, event):
        QApplication.quit()

class GraphWindow(pg.PlotWidget):
    
    def __init__(self, choice, mode):
        super().__init__(parent=None)
        
        self.title="Données capteurs"
        self.setAxisItems(axisItems = {'bottom': pg.DateAxisItem()})
        # Labels axes
        self.abscissa = self.setLabel('bottom', 'Temps')
        self.ordinate =  self.setLabel('left', "Température","°C")
        # Courbe
        self.curve = self.plot(pen='y')
        
        # Données
        self.timestamps = []
        self.temp = np.zeros(30)
        self.hum = np.zeros(30)
        self.lum = np.zeros(30)
        self.mode = mode
        self.choice = choice
        self.update_choice(self.choice)
        self.update_curve(time.time(),0,0,0) ##########

    def update_mode(self,s):
        
        print(s)
    def update_choice(self,s):        
        self.setTitle(s)
        self.removeItem(self.ordinate)
        if s == "Température":
            self.ordinate =  self.setLabel('left', s,"°C")
            self.setYRange(0,35)
        elif s == "Humidité":
            self.ordinate =  self.setLabel('left', s,"%")
            self.setYRange(0,100)
        else:
            self.ordinate =  self.setLabel('left', s,"%")
            self.setYRange(0,100)

    def update_curve(self, timestamp, temp, hum, lum):#, timestamp, temp, hum, lum
        # Stockage
        self.timestamps = np.linspace(timestamp-30, timestamp,30)
      
        self.temp[-1]=temp
        self.hum[-1]=hum
        self.lum[-1]=lum
        data = self.temp
        data[:-1] = data[1:]
        self.curve.setData(self.timestamps, data)
        self.setTitle(self.choice)
        self.curve.setPos(self.timestamps[0], 0)
    

    def make_connection(self, data_object):
        data_object.signal.connect(self.grab_data)

    @Slot(object)
    def grab_data(self, data):
        print(data)
        self.plot.setData(data)


class Worker(QThread):
    signal = Signal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        self.data = [0, 1]
        i = 2
        while True:
            self.data[1] = i
            self.signal.emit(self.data)
            time.sleep(1)
            i += 1


if __name__ == '__main__':

    import sys
   
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
        
    widget = MainWindow(GraphWindow)
    worker = Worker()
    MainWindow.plotwidget.make_connection(worker)
    worker.start()
    sys.exit(app.exec_())

# class LivePlot:
#     def __init__(self):
#         self.app = pg.mkQApp()

#         # Fenêtre
#         self.window = QtWidgets.QWidget()
#         self.layout = QtWidgets.QVBoxLayout()
#         self.window.setLayout(self.layout)

#         # Sélecteur de signal
#         self.selector = QtWidgets.QComboBox()
#         self.selector.addItems(["Température", "Humidité", "Luminosité"])
#         self.layout.addWidget(self.selector)
#         #self.selector.currentTextChanged.connect(self.choice_data)
#         #self.choice = self.selector.currentText()
        
#         #Sélecteur de mode
#         self.modes = QtWidgets.QComboBox()
#         self.modes.addItems(["Simulation","Réél"])
#         self.layout.addWidget(self.modes)
#         #self.modes.currentTextChanged.connect(self.choice_mode)
#         #self.mode = self.modes.currentText()
        
#         # Graphe
#         self.plot = pg.PlotWidget(title="Données capteurs",axisItems = {'bottom': pg.DateAxisItem()})
#         self.layout.addWidget(self.plot)

#         # Label stats
#         self.stats_label = QtWidgets.QLabel("Stats:")
#         self.layout.addWidget(self.stats_label)

#         # Données
#         self.timestamps = []
#         self.temp = np.zeros(30)
#         self.hum = np.zeros(30)
#         self.lum = np.zeros(30)

#         # Courbe
#         self.curve = self.plot.plot(pen='y')

#         # Textes (créés UNE seule fois)
#         self.min_text = pg.TextItem(anchor=(0, 1))
#         self.max_text = pg.TextItem(anchor=(0, 1))
#         self.mean_text = pg.TextItem(anchor=(0, 1))

#         self.plot.addItem(self.min_text)
#         self.plot.addItem(self.max_text)
#         self.plot.addItem(self.mean_text)

#         # Labels axes
#         self.abscissa = self.plot.setLabel('bottom', 'Temps')
#         self.ordinate =  self.plot.setLabel('left', "Température (°C)")
#         #self.ordinate.setXRange(0,35)
#         self.window.show()
        
#     def choice_data(self):
#         choice = self.selector.currentText()
#         return choice
    
#     def choice_mode(self):
#         mode = self.modes.currentText()
#         return mode
    
#     def update(self, timestamps, temp, hum, lum):
#         # Stockage
#         self.timestamps = np.linspace(timestamps-30, timestamps,30)
      
#         self.temp[-1]=temp
#         self.hum[-1]=hum
#         self.lum[-1]=lum

#         choice = self.selector.currentText()
        

#         if choice == "Température":
#             data = self.temp
#             name = "Température (°C)"
#             self.plot.removeItem(self.ordinate)
#             self.ordinate =  self.plot.setLabel('left', name)
#             #self.ordinate.setRange(0,35)
#             self.plot.setYRange(0,35)
#         elif choice == "Humidité":
#             data = self.hum
#             name = "Humidité (%)"
#             self.plot.removeItem(self.ordinate)
#             self.ordinate =  self.plot.setLabel('left', name)
#             #elf.ordinate.setRange(0,35)
#             self.plot.setYRange(0,100)
#         else:
#             data = self.lum
#             name = "Luminosité (%)"
#             self.plot.removeItem(self.ordinate)
#             self.ordinate =  self.plot.setLabel('left', name)
#             #self.ordinate.setRange(0,35)
#             self.plot.setYRange(0,100)
#         # Axe X
#         #x = list(range(len(data)))

#         # Update courbe
#         #print(self.timestamps)
#         print(data)
#         data[:-1] = data[1:]
#         print(data)
#         self.curve.setData(self.timestamps, data)
#         self.plot.setTitle(name)
#         #self.curve.setPos(self.timestamps[0], 0)
        
#         # Stats
#         # if len(data) > 0:
#         #     arr = np.array(data)
#         #     min_val = arr.min()
#         #     max_val = arr.max()
#         #     mean_val = arr.mean()

#         #     # Label texte
#         #     self.stats_label.setText(
#         #         f"{name} | Min: {min_val:.2f} | Max: {max_val:.2f} | Moy: {mean_val:.2f}"
#         #     )

#         #     # Position des textes (à droite du graphe)
#         #     xpos = len(data)

#         #     self.min_text.setText(f"Min: {min_val:.1f}")
#         #     self.min_text.setPos(xpos, min_val)

#         #     self.max_text.setText(f"Max: {max_val:.1f}")
#         #     self.max_text.setPos(xpos, max_val)

#         #     self.mean_text.setText(f"Moy: {mean_val:.1f}")
#         #     self.mean_text.setPos(xpos, mean_val)

#     def run(self):
#         pg.exec()




















































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
        
        
