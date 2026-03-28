# projet-capteur-Python
Interface graphique en Python  pour l’acquisition de capteurs
📊 Projet Capteur - Visualisation de Données
🎯 Objectif

Ce projet permet de lire des données provenant d’un capteur, de les stocker, et de les afficher sous forme de graphique soit en temps réel soit de la mémoire  .

🛠️ Technologies utilisées
Python
▶️ Utilisation
Installer les dépendances :
pip install matplotlib numpy pandas pyqtgraph PyQt6
Lancer le programme :
python main.py
📁 Structure
data_logger.py/programme pour stocker les données lues 
realtime_plot.py/programme pour représenter graphiquement les données en temps réel 
serial_reader.py/programme pour lire les données du capteur (avec possibilité de simulation du capteur)



main.py : programme principal

📈 Résultat

Affichage d’un graphique représentant les données du capteur.
