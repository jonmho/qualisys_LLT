import matplotlib.pyplot as plt
import matplotlib as mpl
import tkinter as tk
from tkinter import filedialog as fd
import time
import numpy as np
import math
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
from statistics import mean
 
max_anzahl_3d_punkte = 2000
zoomfaktor = 100

root = tk.Tk()
root.withdraw()
root.update()
#dateien öffnen
print("Select Qualisys file!")
file = fd.askopenfilename(title='Qualisys-Daten auswählen',initialdir='D:\\FH Aachen\\Lernen\\Abschlussarbeiten\\Praxisprojekt\\Endergebnisse\\',multiple=False,filetypes=(('Ergebnissdateien', '*.txt'), ('All files', '*.*')))
print("Qualisys file: ", file)

print("Select G-code file!")
file_2 = fd.askopenfilename(title='G-Code auswählen',initialdir='D:\\FH Aachen\\Lernen\\Abschlussarbeiten\\Praxisprojekt\\Endergebnisse\\gcode',multiple=False,filetypes=(('G-Code', '*.txt'), ('All files', '*.*')))
print("G-Code file: ", file_2)

#qualisys daten
file_q = open(file, 'r')
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
#print((zeit_q[-1] - zeit_q[0])/1000000000)
freq = int(1000000000 * len(file_ql)/(zeit_q[-1] - zeit_q[0]))

werte_q = list(zip(xwerte_q, ywerte_q, zwerte_q))

erste = [0]
q_diff = [math.sqrt((f[0]-werte_q[c][0])**2 + (f[1]-werte_q[c][1])**2 + (f[2]-werte_q[c][2])**2) for c,f in enumerate(werte_q[1:])]
q_diff = erste + q_diff


#g-code
file_g = open(file_2, 'r')
xgcode = []
ygcode = []
zgcode = []
file_gl = list(file_g)

for l in file_gl[5:-4]: #erste 5 Zeilen überspringen
    ls = l.split(' ')
    if ls[1] == "G04" or ls[1] == "G28.1\n":
        continue
    if ls[2].startswith("F"):
        xgcode.append(float(ls[3][1:]))
        ygcode.append(float(ls[4][1:]))
        zgcode.append(float(ls[5][1:]))
    else:
        xgcode.append(float(ls[2][1:]))
        ygcode.append(float(ls[3][1:]))
        zgcode.append(float(ls[4][1:]))

file_g.close()
for f in file_gl[3].split(' '):
    if f.startswith("F"):
        gesch = int(f[1:])
#gesch = int(file_gl[3].split(' ')[2][1:])
gcode = list(zip(xgcode, ygcode, zgcode))



for c,p in enumerate(q_diff):
    if p > 0.075:
        q_anf = c #erste bewegung
        break

for c,p in enumerate(q_diff[::-1]):
    if p > 0.075:
        q_end = len(q_diff) - c #erste bewegung
        break
    
xwerte_q = xwerte_q[q_anf:q_end]
ywerte_q = ywerte_q[q_anf:q_end]
zwerte_q = zwerte_q[q_anf:q_end]

werte_q = list(zip(xwerte_q, ywerte_q, zwerte_q))

erste = [0]
q_diff = [math.sqrt((f[0]-werte_q[c][0])**2 + (f[1]-werte_q[c][1])**2 + (f[2]-werte_q[c][2])**2) for c,f in enumerate(werte_q[1:])]
q_diff = erste + q_diff
'''
for c,p in enumerate(q_diff):
    if p > 0.075:
        q_anf = c #erste bewegung
        break
'''
q_anf = 0
zeitpunkte = [] #punkte an denen neue linie beginnt
zeitpunkte.append(q_anf)

#g_erste = [[611,-1222,-72.5]] #startpunkt nicht immer hier
g_erste = [tuple([float(i[1:]) for i in file_gl[2].split(' ')[4:7]])]
gcode = g_erste + gcode

for c,g in enumerate(gcode[1:-1]):
    dauer_v = freq * 60 * math.sqrt((g[0]-gcode[c][0])**2 + (g[1]-gcode[c][1])**2 + (g[2]-gcode[c][2])**2)/gesch
    dauer_nach = freq * 60* math.sqrt((g[0]-gcode[c+2][0])**2 + (g[1]-gcode[c+2][1])**2 + (g[2]-gcode[c+2][2])**2)/gesch
    #print(zeitpunkte[-1], dauer_v)
    von = int(zeitpunkte[-1] + dauer_v/2)
    bis = int(zeitpunkte[-1] + dauer_v + dauer_nach/2)
    zp = von + q_diff[von:bis].index(min(q_diff[von:bis]))
    zeitpunkte.append(zp)

zeitpunkte.append(len(werte_q))
#print("zeitpunkte", len(zeitpunkte), zeitpunkte)

schnittpunkte = []
schnittpunkte_2d = []
teilstuecke = []
gcode = np.array(gcode)
for c,t in enumerate(gcode[:-1]):
    u = t-gcode[c+1]
    teilstuecke.append([t,u,gcode[c+1]])

zeitpunkte_neu = zeitpunkte[:]
zeitpunkte_neu[0] = 0
dist_x_list = []
dist_y_list = []
dist_z_list = []


for c,t in enumerate(teilstuecke): #wenn schnittpunkte außerhalb der gerade liegen noch beachten
    for p in werte_q[zeitpunkte_neu[c]:zeitpunkte_neu[c+1]]:
        #lamda = np.sum((-1)*np.dot(t[0]-p, p))/np.sum(np.dot(p,t[1]))
        lamda = (-1)*np.dot(t[0]-p,t[1])/np.dot(t[1],t[1])
        gp = t[0]+lamda*t[1]
        #print(gp,t[0],t[2])
        
        #check if ausserhalb von bereich
        
        if gp[0] > max(t[0][0], t[2][0]): #x
            gp[0] = max(t[0][0], t[2][0])    
        elif gp[0] < min(t[0][0], t[2][0]):
            gp[0] = min(t[0][0], t[2][0])
            
        if gp[1] > max(t[0][1], t[2][1]): #y
            gp[1] = max(t[0][1], t[2][1])    
        elif gp[1] < min(t[0][1], t[2][1]):
            gp[1] = min(t[0][1], t[2][1])
        
        if gp[2] > max(t[0][2], t[2][2]): #z
            gp[2] = max(t[0][2], t[2][2])    
        elif gp[2] < min(t[0][2], t[2][2]):
            gp[2] = min(t[0][2], t[2][2])
        
        dist = np.linalg.norm(gp-p)
        dist_z = gp[2]-p[2]
        dist_z_list.append(dist_z)
        dist_y_list.append(gp[1]-p[1])
        dist_x_list.append(gp[0]-p[0])
        schnittpunkte.append([list(p), list(gp)])
        schnittpunkte_2d.append([list(p)[:2], list(gp)[:2]])

#print(schnittpunkte)

#3d ansicht
schnittpunkte_laenger = [[np.array(a[1]) + zoomfaktor * (np.array(a[0])-np.array(a[1])) ,a[1]] for a in schnittpunkte]
schnittpunkte_2d_laenger = [[np.array(a[1]) + zoomfaktor * (np.array(a[0])-np.array(a[1])) ,a[1]] for a in schnittpunkte_2d]
reduc_fac = int(len(xwerte_q)/max_anzahl_3d_punkte)

#lines = Line3DCollection([i for i in schnittpunkte[::reduc_fac]], color='g', label='Abstände')
lines = Line3DCollection([i for i in schnittpunkte_laenger[::reduc_fac]], color='g', label='Abstände')
#lines_2d = LineCollection(schnittpunkte_2d, color='g',label='Abstände')
lines_2d = LineCollection(schnittpunkte_2d_laenger, color='g',label='Abstände')

print("Reduzierungsfaktor zur Verbesserung der 3D-Ansicht: {}".format(reduc_fac))

#plotten
fig = plt.figure()

#z plot
fig_1, ax_1 = plt.subplots()
#ax_1.plot(xwerte_q, dist_z_list, marker='x', color='g', label='Z Abstände über X')
#ax_1.plot(ywerte_q, dist_z_list, marker='x', color='r', label='Z Abstände über Y')
#ax_1.set(xlabel='x/y', ylabel='z-Wert', title='Z Abstände')
ax_1.plot(dist_z_list, marker='x', color='r', linestyle='None', label='Z Abstände')
ax_1.plot(dist_y_list, marker='x', color='b', linestyle='None', label='Y Abstände')
ax_1.plot(dist_x_list, marker='x', color='g', linestyle='None', label='X Abstände')
ax_1.set(xlabel='Messwert-ID', ylabel='Abstand zur Soll-Position [mm]')
ax_1.grid()
ax_1.legend()

#z über x und y
'''
fig_4, (ax_4,ax_5) = plt.subplots(1,2)
ax_4.plot(xwerte_q, dist_z_list, marker='x', color='g', label='Z Abstände über X')
ax_5.plot(ywerte_q, dist_z_list, marker='x', color='r', label='Z Abstände über Y')
ax_4.set(xlabel='x', ylabel='z-Wert', title='Z Abstände')
ax_5.set(xlabel='y', ylabel='z-Wert', title='Z Abstände')
ax_4.grid()
ax_4.legend()
ax_5.grid()
ax_5.legend()
'''
#2d plot
fig_2, ax_2 = plt.subplots()
#ax_2.add_collection(lines_2d)
ax_2.plot([i[0] for i in gcode], [i[1] for i in gcode], marker='x', color='r', label="G-Code")
#ax_2.plot(xwerte_q, ywerte_q, marker='o', color='b', linestyle='None', label="Qualisys")
#ax_2.scatter(xwerte_q, ywerte_q, marker='o', label="Qualisys", cmap=mpl.colormaps["hsv"], c=range(len(xwerte_q)))
#ax_2.scatter(xwerte_q, ywerte_q, marker='o', label="Qualisys")
ax_2.set(xlabel='x [mm]', ylabel='y [mm]')
#ax_2.grid()
ax_2.legend()

#3d plot

ax_3 = fig.add_subplot(projection='3d')
#ax_3.add_collection(lines)
ax_3.plot([i[0] for i in gcode], [i[1] for i in gcode], [i[2] for i in gcode], marker='x', color='r', label="G-Code")
#ax_3.plot(xwerte_q, ywerte_q, zwerte_q, marker='o', color='b', linestyle='None', label="Qualisys")
ax_3.set_proj_type('ortho')
ax_3.set(xlabel='x [mm]', ylabel='y [mm]', zlabel='z [mm]')
ax_3.grid()
ax_3.legend()

fig_6, ax_6 = plt.subplots()
ax_6.plot(q_diff, marker='x', color='b', linestyle='None', label="Qualisys")
ax_6.set(xlabel='Messwert-ID', ylabel='Abstand zum Vorgänger [mm]')
ax_6.grid()
for item in ([ax_6.title, ax_6.xaxis.label, ax_6.yaxis.label] +
             ax_6.get_xticklabels() + ax_6.get_yticklabels()):

    item.set_fontsize(14)

#ax.set(xlabel='x', ylabel='y', zlabel='z', title='G-Code und Qualisys')
#plt.xlim([min(xwerte_q)-100,max(xwerte_q)+100])
#plt.ylim([min(ywerte_q)-100,max(ywerte_q)+100])
#ax.set_zlim([min(zwerte_q)-100,max(zwerte_q)+100])
#ax.set_ylim([0, max(q_diff)])
#ax_1.axis('equal')
ax_2.axis('equal')
ax_3.axis('equal')
#ax_4.axis('equal')
#ax_5.axis('equal')

dist_x_abs = [abs(i) for i in dist_x_list]
dist_y_abs = [abs(i) for i in dist_y_list]
dist_z_abs = [abs(i) for i in dist_z_list]
dist_gesamt = [math.sqrt(a[0]**2 + a[1]**2 + a[2]**2) for a in zip(dist_x_abs,dist_y_abs,dist_z_abs)]
print("Durchschnittliche Abweichung: \n-x-Richtung: {}\n-y-Richtung: {}\n-z-Richtung: {}\n-Gesamt: {}".format(mean(dist_x_abs), mean(dist_y_abs), mean(dist_z_abs), mean(dist_gesamt)))
print("Maximale Abweichug:\n-x-Richtung: {}\n-y-Richtung: {}\n-z-Richtung: {}\n-Gesamt: {}".format(max(dist_x_abs),max(dist_y_abs),max(dist_z_abs),max(dist_gesamt)))
#print(q_anf,len(werte_q))
#print("zeitpunkte", len(zeitpunkte), zeitpunkte)
plt.show()
