# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:20:12 2026

@author: Majdo
"""

import csv
import os

def save_data(base_folder, timestamp, temp, hum, lum):
    os.makedirs(base_folder, exist_ok=True)
    # Nom du fichier basé sur la date (ex: 2026-03-28.csv)
    filename = f"{timestamp.strftime('%Y-%m-%d')}.csv"
    filepath = os.path.join(base_folder, filename)
    

    file_exists = os.path.isfile(filepath)

    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)

        # Si le fichier n'existe pas → écrire l'en-tête
        if not file_exists:
            writer.writerow(["Timestamp", "Temp(°C)", "Hum(%)", "Lum(%)"])

        # Ajouter la ligne
        writer.writerow([
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            temp, hum, lum
        ])