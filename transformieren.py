import numpy as np
import math
from numpy.linalg import norm
from statistics import mean
from tkinter import filedialog as fd

def intersect(line_1, line_2): # line_1 = [[0,0],[1,1]]
    steig1 = line_1[0]-line_1[1]
    #steig2 = line_2[0]-line_2[1]
    A = np.vstack([line_1[0]-line_1[1], -(line_2[0] - line_2[1])]).T
    b = line_2[0]-line_1[0]
    try:
        R = np.linalg.solve(A,b)
        #print(R)
        return line_1[0] + R[0] * steig1, None
    except np.linalg.LinAlgError:
        #print("parallel")
        return None, steig1
    except:
        print("anderer Fehler")
    
#blender_prepare.py
print("Select Raster file!")
file = fd.askopenfilename(title='Rasterdatei auswählen',initialdir='C:\\Users\\LAPTOP845_LGORISSEN\\Documents\\Qualisys\\python_neu\\Versuchspakete',multiple=False,filetypes=(('Ergebnissdateien', '*.txt'), ('All files', '*.*')))
#file = "C:/Users/LAPTOP845_LGORISSEN/Documents/Qualisys/python_neu/python/stepcraft/ergebnisse/2023.04.04_15.05_raster_1_4_8000.txt"
print("Raster file: ", file)

#print("Select G-code file!")
#file_2 = fd.askopenfilename(title='G-Code auswählen',initialdir='C:\\Users\\LAPTOP845_LGORISSEN\\Documents\\Qualisys\\python_neu\\cnc_gcode',multiple=False,filetypes=(('G-Code', '*.txt'), ('All files', '*.*')))
file_2 = "C:/Users/LAPTOP845_LGORISSEN/Documents/Qualisys/python_neu/cnc_gcode/raster_1_4_8000.txt"
print("G-Code file: ", file_2)

#file_3 = "C:/Users/LAPTOP845_LGORISSEN/Documents/Qualisys/python_neu/python/stepcraft/ergebnisse/2023.04.04_15.47_y_8000_0_neukal.txt"
print("Select Qualisys file!")
file_3 = fd.askopenfilename(title='Qualisys-Daten auswählen',initialdir='C:\\Users\\LAPTOP845_LGORISSEN\\Documents\\Qualisys\\python_neu\\Versuchspakete',multiple=False,filetypes=(('Rasterdatei', '*.txt'), ('All files', '*.*')))
print("Qualisys file: ", file_3)

#gcode einlesen
file_g = open(file_2, 'r')
xgcode = []
ygcode = []
zgcode = []
file_gl = list(file_g)

anzahl = 1 #erstes mal g28 wird nicht mitgezählt, da file_gl[3:-2]
for l in file_gl[3:-2]:
    ls = l.split(' ')
   
    if ls[1] == "G04":
        continue
    if ls[1] == "G28.1\n":
        anzahl +=1
        continue
    if anzahl ==1:
        if ls[2].startswith("F"):
            xgcode.append(float(ls[3][1:]))
            ygcode.append(float(ls[4][1:]))
            zgcode.append(float(ls[5][1:]))
        else:
            xgcode.append(float(ls[2][1:]))
            ygcode.append(float(ls[3][1:]))
            zgcode.append(float(ls[4][1:]))
#dimensionen bestimmen
resx = int([i for i in np.roots([2,3,1-len(xgcode)]) if i > 0][0]) -1
resy = 2 * resx
print("resolution: ",resx,resy)
file_g.close()

#qualisys daten bahn
file_q_3 = open(file_3, 'r')
xwerte_q_3 = []
ywerte_q_3 = []
zwerte_q_3 = []
zeit_q_3 = []
file_ql_3 = list(file_q_3)
for l in file_ql_3:
    l = l.split(',')
    xwerte_q_3.append(float(l[0]))
    ywerte_q_3.append(float(l[1])) 
    zwerte_q_3.append(float(l[2])) 
    zeit_q_3.append(int(l[3]))
file_q_3.close()
werte_q_3 = list(zip(xwerte_q_3, ywerte_q_3, zwerte_q_3))

#qualisys daten ecken
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
#q_diff für alle werte aufstellen & einzelne fahrten trennen
werte_q = list(zip(xwerte_q, ywerte_q, zwerte_q))
erste = [0]
q_diff = [math.sqrt((f[0]-werte_q[c][0])**2 + (f[1]-werte_q[c][1])**2 + (f[2]-werte_q[c][2])**2) for c,f in enumerate(werte_q[1:])]
q_diff = erste + q_diff
freq = int(1000000000 * len(file_ql)/(zeit_q[-1] - zeit_q[0]))

cl = 0
zeitpunkte = [0]
counter = 0
for i,t in enumerate(q_diff):
    if cl == 0 and t >= 0.075:
        #zeitpunkte.append(i)
        cl += 1
        continue
    if cl > 0 and t < 0.075:
        if counter == 0:
            z_anf = i
        counter +=1
        
        if counter == (int(freq * 4.5)):
            zeitpunkte.append(z_anf+int(2.5*freq)) #damit letzte pause auch erkannt wird
    if t >= 0.075:
        #if counter >= (freq * 4.5):
            #zeitpunkte.append(i)
        counter = 0
#letztes stück erkannt?        
if len(zeitpunkte) < anzahl+1:
    zeitpunkte.append(len(q_diff))
print("zuordnen")   
#punktezuordnungsliste
pliste = []
resx1 = resx+1
resy1 = resy+1
gesamt = resx1*resy1-1
vor = True
for x in range(resx1):
    for y in range(resy1):
        if vor:
            pliste.append(x*resy1+y)
        if not vor:
            pliste.append((x+1)*resy1-(y+1))
    vor = not vor

vor = False
if resx1%2==1:
    for y in range(resy1):
        for x in range(resx1):
            if x == 0 and y == 0:
                continue
            if not vor:
                pliste.append(gesamt-(x*resy1)-y)
            if vor:
                pliste.append((x+1)*resy1 -(y+1))
        vor = not vor
if resx1%2==0:
    for y in range(resy1):
        for x in range(resx1):
            if x == 0 and y == 0:
                continue
            if not vor:
                pliste.append(gesamt-(x+1)*resy1+(y+1))
            if vor:
                pliste.append(x*resy1+y)
        vor = not vor
        
#leere liste vorbereiten
ecken_all = []
for d in range(gesamt+1):
    ecken_all.append([])
    
print("teilstücke durchgehen")
#teilstücke durchgehen    
for z,z1 in zip(zeitpunkte,zeitpunkte[1:]):
    teilwerte_q = werte_q[z:z1]
    teilq_diff = q_diff[z:z1]
    teil_zeitpunkte = []
    for i,t in enumerate(teilq_diff):
        if t < 0.1:
            counter +=1

        if t >= 0.1:
            if counter >= int(freq * 2):
                teil_zeitpunkte.append(i)
            counter = 0
        if i == len(teilq_diff)-1 and counter >=int(freq*2):
            teil_zeitpunkte.append(i)
    
    for c,k in zip(pliste,teil_zeitpunkte):
        ecken_all[c].append([mean([p[0] for p in teilwerte_q[k-int(2*freq)+10:k-10]]),
                           mean([p[1] for p in teilwerte_q[k-int(2*freq)+10:k-10]]),
                           mean([p[2] for p in teilwerte_q[k-int(2*freq)+10:k-10]])])
  
for c,eck in enumerate(ecken_all):
    ecken_all[c] = np.array([mean([p[0] for p in eck]),
           mean([p[1] for p in eck]),
           mean([p[2] for p in eck])])

#ecken_all = np.array([[0,0,2],[10,0,2],[15,10,2],[10,10,2],[19,1,3],[21,12,3],[20,19,1],[13,21,1],[5,18,2]])
#ecken_all = np.array([[0,0,2],[10,10,2],[5,18,2],[10,0,2],[15,10,2],[13,21,1],[19,1,3],[21,12,3],[20,19,1]])
Mpunkte = np.ndarray(shape=(resx+1,resy+1),dtype=np.ndarray)
x = 0
y = 0
Mgeraden = np.ndarray(shape=(resx,resy),dtype=np.ndarray)

for e in ecken_all:
    Mpunkte[x,y] = e
    y = int((y+1)%(resy+1))
    if y == 0:
        x += 1
        
#faces &geraden aufstellen
print("faces und geraden")
faces = []
for x in range(resx):
    for y in range(resy):
        Mp = [Mpunkte[x,y],Mpunkte[x+1,y],Mpunkte[x+1,y+1],Mpunkte[x,y+1]]
        faces.append([x*(resy+1)+y,(x+1)*(resy+1)+y, (x+1)*(resy+1)+y+1, x*(resy+1)+y+1])
        
        xus = (Mp[0][:2]-Mp[1][:2])[1]/(Mp[0][:2]-Mp[1][:2])[0]
        xu = [xus,Mp[0][1]-Mp[0][0]*xus]
        
        xos = (Mp[2][:2]-Mp[3][:2])[1]/(Mp[2][:2]-Mp[3][:2])[0]
        xo = [xos,Mp[2][1]-Mp[2][0]*xos]
        
        yus = (Mp[0][:2]-Mp[3][:2])[1]/(Mp[0][:2]-Mp[3][:2])[0]
        yu = [yus,Mp[0][1]-Mp[0][0]*yus]
        
        yos = (Mp[1][:2]-Mp[2][:2])[1]/(Mp[1][:2]-Mp[2][:2])[0]
        yo = [yos,Mp[1][1]-Mp[1][0]*yos]
        
        Mgeraden[x,y] = np.array([xu,xo,yu,yo])


faces = np.array(faces)

#punkte_all = np.array([[6.875,4,714],[27,1230,713],[-400,400,713],[-600,-1300,700]])
punkte_all = np.array(werte_q_3)
punkte_all_alt = np.copy(punkte_all)

punktexy_all = np.array([[i[0],i[1]] for i in punkte_all])
edges = []

#idealecken aufstellen
idealecken_all = []
xt = 1222/resx
yt = 2444/resy
for x in range(resx1):
    for y in range(resy1):
        idealecken_all.append([x*xt, y*yt, 0])
#idealecken_all = np.array([[0,0,0],[0,10,0],[00,20,0],[10,0,0],[10,10,0],[10,20,0],[20,0,0],[20,10,0],[20,20,0]])

print("punkte zuweisen")
#punkte zuweisen
punkte_g = np.ndarray(shape=(resx,resy),dtype=list)
for i in range(resx):
    for j in range(resy):
        punkte_g[i,j]=[]
        
for c,p in enumerate(punktexy_all):
    for c1,a in enumerate(Mgeraden):
        for c2,b in enumerate(a):
            xu = (p[0]*b[0][0]+b[0][1])
            xo = (p[0]*b[1][0]+b[1][1])
            yu = ((p[1]-b[2][1])/b[2][0]) 
            yo = ((p[1]-b[3][1])/b[3][0])
            if c2 == 0:
                xu = -999999999
            if c1 == 0:
                yu = -999999999
            if c2 == int(resy-1):
                xo = 999999999
            if c1 == int(resx-1):
                yo = 999999999
            #print("p: ",p, "xu: ",xu, "xo: ",xo, "yu: ",yu, "yo: ",yo)
            if p[1] >= xu and p[1] < xo and p[0] >= yu and p[0] < yo:
                #print("punkt hier: ",p[1], xu,xo,p[0],yu,yo, c1, c2, resx, resy)
                punkte_g[c1,c2].append(c)
    if c%10000==0:
        print(c, "punkte geschafft")
#print(punkte_g)
#punkte ordnen
#print(li[li[:, 1].argsort()])
print("punkte verzerren")

#verzerrung     punkte noch geben
for i,f in enumerate(faces):
    ecken = np.array([ecken_all[c] for c in f])
    idealecken = np.array([idealecken_all[c] for c in f])
    punkt1 = ecken[0] - idealecken[0]
    
    #punkte = []
    #punktexy = []          
    #punkte = np.array([ve - punkt1 for ve in punkte])
    ecken = np.array([ve - punkt1 for ve in ecken])
    eckenxy = np.array([e[:2] for e in ecken])
    schnittpunkt1 = (intersect([eckenxy[0],eckenxy[1]],[eckenxy[2],eckenxy[3]])) #[x,y], [sx,xy]
    schnittpunkt2 = (intersect([eckenxy[0],eckenxy[3]],[eckenxy[2],eckenxy[1]]))
    punkt2 = - ecken[1] + idealecken[1]
    punkt3 = - ecken[2] + idealecken[2]
    punkt4 = - ecken[3] + idealecken[3]
    p_mit_v = []
    p_g = punkte_g[int(i/resy),i%resy]
    for c,p in enumerate(zip(punktexy_all, punkte_all)):
        if c in p_g:
            p1 = p[1] - punkt1
            p0 = p[0] - punkt1[:2]
            if norm(schnittpunkt1[1] == None) == 1:
                r1u = intersect([p0, schnittpunkt1[0]],[eckenxy[0],eckenxy[3]])[0]
                r1o = intersect([p0, schnittpunkt1[0]],[eckenxy[1],eckenxy[2]])[0]
            elif norm(schnittpunkt1[1] == None) == 0:
                r1u = intersect([p0, p0 + schnittpunkt1[1]],[eckenxy[0],eckenxy[3]])[0]
                r1o = intersect([p0, p0 + schnittpunkt1[1]],[eckenxy[1],eckenxy[2]])[0]
                
            if norm(schnittpunkt2[1] == None) == 1:
                r2u = intersect([p0, schnittpunkt2[0]],[eckenxy[0],eckenxy[1]])[0]
                r2o = intersect([p0, schnittpunkt2[0]],[eckenxy[2],eckenxy[3]])[0]
            elif norm(schnittpunkt2[1] == None) == 0:
                r2u = intersect([p0, p0 + schnittpunkt2[1]],[eckenxy[0],eckenxy[1]])[0]
                r2o = intersect([p0, p0 + schnittpunkt2[1]],[eckenxy[2],eckenxy[3]])[0]
            r1neg = max(norm(r1o-p0)/norm(r1o-r1u),0)
            r1pos = max(norm(p0-r1u)/norm(r1o-r1u),0)
            r2neg = max(norm(r2o-p0)/norm(r2o-r2u),0)
            r2pos = max(norm(p0-r2u)/norm(r2o-r2u),0)
            #p_mit_v.append(p[1] + r1pos*r2neg*punkt2 + r1pos*r2pos*punkt3 + r1neg*r2pos*punkt4) 
            punkte_all[c]= p1 + r1pos*r2neg*punkt2 + r1pos*r2pos*punkt3 + r1neg*r2pos*punkt4
    print(i+1, "faces geschafft")

'''
x=1
y=1
for p in punkte_g:
    for g in p:
        print("x:",x,"y:",y,"punkte: ",g)
        y += 1
    y = 1
    x += 1
'''
verzerrt_name = file_3[:-4] + "_verzerrt_2.txt"
datei = open(verzerrt_name, 'w')
for c,p in enumerate(punkte_all):
    datei.write(str(p[0]) + "," + str(p[1]) + "," + str(p[2]) + "," + str(zeit_q_3[c]) + "\n")
datei.close()

