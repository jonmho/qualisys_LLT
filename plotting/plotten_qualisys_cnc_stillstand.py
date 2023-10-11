import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog as fd
import time
import numpy as np
import math
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
from statistics import mean
import matplotlib as mpl
import matplotlib.dates as md
from datetime import timedelta
import dateutil
from scipy.stats import norm
import statistics
 
root = tk.Tk()
root.withdraw()
root.update()
#dateien öffnen
print("Select Qualisys file!")
file = fd.askopenfilename(title='Qualisys-Daten auswählen',initialdir='D:\\FH Aachen\\Lernen\\Abschlussarbeiten\\Praxisprojekt\\Endergebnisse\\',multiple=False,filetypes=(('Ergebnissdateien', '*.txt'), ('All files', '*.*')))

print("Qualisys file: ", file)
fac = int(input("Reduzierungsfaktor eingeben!\n"))
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

werte_q = list(zip(xwerte_q, ywerte_q, zwerte_q))
print(werte_q)
erste = [0]
q_diff = [math.sqrt((f[0]-werte_q[c][0])**2 + (f[1]-werte_q[c][1])**2 + (f[2]-werte_q[c][2])**2) for c,f in enumerate(werte_q[1:])]
q_diff = erste + q_diff

x_anf = mean(xwerte_q[:10])
y_anf = mean(ywerte_q[:10])
z_anf = mean(zwerte_q[:10])
anf_diff = [math.sqrt((f[0]-x_anf)**2 + (f[1]-y_anf)**2 + (f[2]-z_anf)**2)for f in werte_q]
zeit_anf = zeit_q[0]
print("Vergangene Zeit: ", timedelta(seconds=(zeit_q[-1]-zeit_q[0])/1000000000))


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(xwerte_q[::fac], ywerte_q[::fac], zwerte_q[::fac], cmap=mpl.colormaps["hsv"], c=range(len(xwerte_q[::fac])), label="Qualisys")
ax.set_proj_type('ortho')
ax.set(xlabel='x', ylabel='y', zlabel='z')
ax.grid()
ax.legend()
ax.set_xlim([-625,1875])
ax.set_ylim([0,2500])
#ax.axis('equal')


'''
xfmt = md.DateFormatter('%H:%M:%S')
fig_2, ax_2 = plt.subplots()
ax_2.xaxis.set_major_formatter(xfmt)
datestrings = [str(timedelta(seconds=(i-zeit_anf)/1000000000)) for i in zeit_q]
dates = [dateutil.parser.parse(s) for s in datestrings]

fig_1, ax_1 = plt.subplots()
ax_1.xaxis.set_major_formatter(xfmt)
ax_1.plot(q_diff,marker='x',linestyle='None')
ax_1.grid()
ax_1.set(xlabel='Zeit [hh:mm:ss]', ylabel='Abstand zum Vorgänger [mm]', title='q_diff')


ax_2.scatter(dates[::fac],anf_diff[::fac], marker='x')
ax_2.grid()
ax_2.set(xlabel='Zeit [hh:mm:ss]', ylabel='Abstand zum Startpunkt [mm]')
#ax_2.set_xlim(x['Time'][0],x['Time'][35])
ax_2.set_ylim([0,1.25])
ax_2.set_xlim([dates[0],dates[-1]])

for item in ([ax_2.title, ax_2.xaxis.label, ax_2.yaxis.label] +
             ax_2.get_xticklabels() + ax_2.get_yticklabels()):

    item.set_fontsize(14)


plt.show()

 #letzen 7000 werte
x_anf = mean(xwerte_q[-7000:])
y_anf = mean(ywerte_q[-7000:])
z_anf = mean(zwerte_q[-7000:])
anf_diff = [math.sqrt((f[0]-x_anf)**2 + (f[1]-y_anf)**2 + (f[2]-z_anf)**2)for f in werte_q[-7000:]]
bins = np.linspace(0, 0.08, 200)
fig, ax = plt.subplots()
ax.hist(anf_diff,bins, align='mid', ec='black')
ax.set(xlabel='Abweichung [mm]', ylabel='Häufigkeit')
print("stdabw: ", np.std(anf_diff), statistics.mean(anf_diff), mean(anf_diff))
mu, std = norm.fit(anf_diff)
x = np.linspace(-0.02, 0.08, 100)
p = norm.pdf(x, mu, std)
ax.set_xlim(left=0, right=0.075)
#ax.plot(x, p)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):

    item.set_fontsize(14)
'''
plt.show()
