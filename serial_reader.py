# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:17:56 2026

@author: Majdo
"""
import serial

import time
import random
import numpy as np

def read_serial(mode="sim", port='COM3', baudrate=9600):
    
    if mode == "real":
        
        try:
            # Ouvrir le port série (remplace 'COM7' par ton port réel)
            ser = serial.Serial('COM4', 9600, timeout=1)
        
            print("Lecture en cours... (Ctrl+C pour arrêter)")
        
            while True:
                line =  ser.readline().decode().strip()  # Lire et décoder la ligne reçue
                if line:  # Vérifier si la ligne n'est pas vide
                    yield line  # Aff icher les données reçues

        except serial.SerialException as e:
             print(f"Erreur d'accès au port série : {e}")
        
        except KeyboardInterrupt:
            print("\nArrêt du programme.")

    elif mode == "sim":
        print("Mode simulation activé")
        t = 0
        while True:
            temp = 25 + 3 * np.sin(t/10) + random.uniform(-1, 1)
            hum = 60 + 10 * np.sin(t/15) + random.uniform(-1, 1)
            lum = 50 + 20 * np.sin(t/5) + random.uniform(-1, 1)

            line = f"{round(temp,1)} {round(hum)} {round(lum)}"
            
            yield line
            
            t += 1
            time.sleep(1) # 1 mesure par seconde

        # except serial.SerialException as e:
        #      print(f"Erreur d'accès au port série : {e}")
        
        # except KeyboardInterrupt:
        #     print("\nArrêt du programme.")
        
        # finally:
        #     if 'ser' in locals() and ser.is_open:
        #         ser.close()  # Fermer proprement le port série
        
        
# def read_serial(port='COM17', baudrate=9600):
#     ser = serial.Serial(port, baudrate, timeout=1)

#     try:
#         while True:
#             line = ser.readline().decode().strip()
#             if line:
#                 yield line

#     finally:
#         ser.close()