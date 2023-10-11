import tkinter as tk
from tkinter import filedialog as fd
import numpy as np
import os

root = tk.Tk()
root.withdraw()
root.update()

print("Select Qualisys file!")
file = fd.askopenfilename(title='Qualisys-Daten auswählen',initialdir='D:\\FH Aachen\\Lernen\\Abschlussarbeiten\\Praxisprojekt\\Endergebnisse\\',multiple=True,filetypes=(('Ergebnissdateien', '*.txt'), ('All files', '*.*')))
print("Qualisys files: ", file)
print("Kalibrationsdatei auswählen!")
file_kal = fd.askopenfilename(title='Kalibrationsdatei auswählen',initialdir='D:\\FH Aachen\\Lernen\\Abschlussarbeiten\\Praxisprojekt\\Endergebnisse\\',filetypes=(('Kalibrationsdatei', '*.txt'), ('All files', '*.*')))
print("Kalibrations file: ", file_kal)

kal = open(file_kal, 'r')
kal_list = []
for i in list(kal):
    kal_list.append([float(k) for k in i.split(',')])
    
drehmatrix_ebene = np.array([kal_list[0], kal_list[1], kal_list[2]])
drehmatrix_z = np.array([kal_list[3], kal_list[4], kal_list[5]])
translate = np.array(kal_list[6])
xskal = np.array(kal_list[7][0])
yskal = np.array(kal_list[7][1])

#werte=np.array([robot.x, robot.y, robot.z])
for t in file:
    head,tail = os.path.split(t)
    file_q = open(t, 'r')
    xwerte_q = []
    ywerte_q = []
    zwerte_q = []
    zeit_q = []


    file_ql = list(file_q)
    for l in file_ql:
        l = l.split(',')
        xwerte_q.append(float(l[0]))
        ywerte_q.append(float(l[1])) 
        zwerte_q.append(float(l[2])) 
        zeit_q.append(int(l[3]))
    file_q.close()

    werte_q = list(zip(xwerte_q, ywerte_q, zwerte_q))

    #verzerrt_name = t[:-4] + "_helmert_skal.txt"
    verzerrt_name = os.path.join(head[:-4] + "/helmert", tail[:-4] + "_helmert_skal.txt")
    datei = open(verzerrt_name, 'w')
    for c,p in enumerate(werte_q):
        werte_e = np.matmul(drehmatrix_ebene, np.array(p))
        werte_d = np.matmul(drehmatrix_z, werte_e)
        xwert,ywert,zwert = werte_d+translate
        xwert = xwert * xskal
        ywert = ywert * yskal
        datei.write(str(xwert) + "," + str(ywert) + "," + str(zwert) + "," + str(zeit_q[c]) + "\n")
    datei.close()

    print("Datei geschrieben: ", verzerrt_name)

