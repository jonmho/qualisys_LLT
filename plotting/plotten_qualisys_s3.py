import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog as fd
import numpy as np
import math
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from statistics import mean
import matplotlib as mpl
bxlist2 = []
root = tk.Tk()
root.withdraw()
root.update()
#dateien öffnen

print("Select Qualisys file!")
filelist = fd.askopenfilename(title='Qualisys-Daten auswählen',initialdir='C:\\Users\\LAPTOP845_LGORISSEN\\Documents\\Qualisys\\python_neu\\Versuchspakete',multiple=True,filetypes=(('Ergebnissdateien', '*.txt'), ('All files', '*.*')))
print("Qualisys file: ", filelist)

print("Select G-code file!")
file_2 = fd.askopenfilename(title='G-Code auswählen',initialdir='C:\\Users\\LAPTOP845_LGORISSEN\\Documents\\Qualisys\\python_neu\\Versuchspakete\\gcode',multiple=False,filetypes=(('G-Code', '*.txt'), ('All files', '*.*')))
print("G-Code file: ", file_2)

#qualisys daten
bxlist = []
for file in filelist:
    try:
        print(file)
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

        #q_diff aufstellen
        erste = [0]
        q_diff = [math.sqrt((f[0]-werte_q[c][0])**2 + (f[1]-werte_q[c][1])**2 + (f[2]-werte_q[c][2])**2) for c,f in enumerate(werte_q[1:])]
        q_diff = erste + q_diff

        #g-code
        file_g = open(file_2, 'r')
        xgcode = []
        ygcode = []
        zgcode = []
        file_gl = list(file_g)

        for l in file_gl[5:-2]: #erste 5 Zeilen überspringen
            ls = l.split(' ')
            #if ls[1] == "G04" or ls[1] == "G28.1\n" or ls[2].startswith("F"):
            #print(ls)
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
        gcode = list(zip(xgcode, ygcode, zgcode))

        #frequenz und geschwindigkeit
        freq = int(1000000000 * len(file_ql)/(zeit_q[-1] - zeit_q[0]))
        for f in file_gl[3].split(' '):
            if f.startswith("F"):
                gesch = int(f[1:])
                
        #q_diff auswerten, punkte(pausen) erkennen
        for c,p in enumerate(q_diff):
            if p > 0.075:
                q_anf = c #erste bewegung
                break

        counter = 0
        zeitpunkte = []
        z_anf = 0
        #anfang hinzufügen
        zeitpunkte.append(0)
        zeitpunkte.append(q_anf)

        for a,qd in enumerate(q_diff):
            if a >= q_anf:
                if qd < 0.075:
                    if counter == 0:
                        z_anf = a
                        
                    counter += 1
                    
                    if counter == int(freq * 2):
                        zeitpunkte.append(z_anf)
                        
                elif qd >= 0.075 and counter > int(freq * 2):
                    zeitpunkte.append(a)
                    counter = 0
                    
                elif qd >= 0.075:
                    counter = 0
                    
        #ende hinzufügen            
        zeitpunkte.append(len(q_diff))
        #print("Anzahl erkannter Pausen: ",len(zeitpunkte),zeitpunkte)

        zeitpunkte_mittelpunkt = [i for c,i in enumerate(zeitpunkte) if (c%4 != 3 and c%4 != 2)]
        #print(len(zeitpunkte_mittelpunkt), zeitpunkte_mittelpunkt)
        mittelpunkte = []
        mittel_x = []
        mittel_y = []
        mittel_z = []
        #print(len(zeitpunkte))
        for t in range(17):
            
            m_x = mean(xwerte_q[zeitpunkte_mittelpunkt[t*2]+10:zeitpunkte_mittelpunkt[t*2+1]-10])
            m_y = mean(ywerte_q[zeitpunkte_mittelpunkt[t*2]+10:zeitpunkte_mittelpunkt[t*2+1]-10])
            m_z = mean(zwerte_q[zeitpunkte_mittelpunkt[t*2]+10:zeitpunkte_mittelpunkt[t*2+1]-10])
            mittel_x.append(m_x)
            mittel_y.append(m_y)
            mittel_z.append(m_z)
            mittelpunkte.append([m_x, m_y, m_z])
            
        #print(*mittelpunkte)

        stdabw = math.sqrt(sum(np.var(np.column_stack((mittel_x,mittel_y,mittel_z)),axis=0)))

        schwerpunkt = [mean(mittel_x), mean(mittel_y), mean(mittel_z)]
        boxplotlist = [math.sqrt((m[0]-schwerpunkt[0])**2 + (m[1]-schwerpunkt[1])**2 + (m[2]-schwerpunkt[2])**2) for m in mittelpunkte]
        for b in boxplotlist:
            bxlist.append(b)
        
    except:
        print("fail")
        continue
'''
for c,m in enumerate(mittelpunkte):
    print("Punkt{}: {}, {}, {}\t".format(c+1, m[0], m[1], m[2]), "Abstand zum Schwerpunkt: ", math.sqrt((m[0]-schwerpunkt[0])**2 + (m[1]-schwerpunkt[1])**2 + (m[2]-schwerpunkt[2])**2),"\n")
    #print("Abstand zum Schwerpunkt: ", math.sqrt((m[0]-schwerpunkt[0])**2 + (m[1]-schwerpunkt[1])**2 + (m[2]-schwerpunkt[2])**2),"\n")
print("Schwerpunkt: ",schwerpunkt)
print("Standartabweichung gesamt:", stdabw, " x:",math.sqrt(np.var(mittel_x)), "y:",math.sqrt(np.var(mittel_y)), "z:",math.sqrt(np.var(mittel_z)))
print("Alle Angaben in mm!")
'''
fig, ax = plt.subplots()
erg = ax.boxplot(bxlist)
ax.set(ylabel='Abstand zum Schwerpunkt [mm]')
print("median:",ax.boxplot(bxlist)['medians'][0].get_ydata())
print("whisker", [i.get_ydata() for i in ax.boxplot(bxlist)['whiskers']])
print("box", [i.get_ydata() for i in ax.boxplot(bxlist)['boxes']])
print("fliers", [i.get_ydata() for i in ax.boxplot(bxlist)['fliers']])
#ax.set_ylim([0,max(bxlist)*1.1])
ax.set_ylim(bottom=0, top=max(bxlist)*1.1)
ax.grid(axis='y')
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):

    item.set_fontsize(14)
plt.show()
