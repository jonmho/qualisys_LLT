import time
from statistics import mean
import numpy as np
from skspatial.objects import Plane
import math
from tkinter import filedialog as fd

#Messung nicht direkt starten, sondern System zur Ruhe kommen lassen, 157 & 103 für pfad_xy, 122 & 147 Grenze bei 0.05 statt 0.1
     
def koord_trans(xwerte_q, ywerte_q, zwerte_q, freq):
    werte_ql = list(zip(xwerte_q, ywerte_q, zwerte_q))
    erste_l = [0]
    ql_diff = [math.sqrt((f[0]-werte_ql[c][0])**2 + (f[1]-werte_ql[c][1])**2 + (f[2]-werte_ql[c][2])**2) for c,f in enumerate(werte_ql[1:])]
    ql_diff = erste_l + ql_diff
    
    cl = 0
    zl = []
    counter = 0
    for i,t in enumerate(ql_diff):
        if cl == 0 and t >= 0.075:
            zl.append(i)
            cl += 1
            continue
        if cl > 0 and t < 0.075:
            if counter == 0:
                z_anf = i
            counter +=1
            if counter == int(freq * 1.5):
                zl.append(z_anf)
        if t >= 0.075:
            if counter >= (freq * 1.5):
                zl.append(i)
            counter = 0
    print("zl zeitpunkte: ", zl)
    x_punkte = xwerte_q[:zl[0]] + xwerte_q[zl[1]:zl[2]] + xwerte_q[zl[3]:zl[4]]
    y_punkte = ywerte_q[:zl[0]] + ywerte_q[zl[1]:zl[2]] + ywerte_q[zl[3]:zl[4]]
    z_punkte = zwerte_q[:zl[0]] + zwerte_q[zl[1]:zl[2]] + zwerte_q[zl[3]:zl[4]]
    #skalierung
    xskal = 1222/math.sqrt((mean(xwerte_q[:zl[0]])-mean(xwerte_q[zl[1]:zl[2]]))**2 + (mean(ywerte_q[:zl[0]])-mean(ywerte_q[zl[1]:zl[2]]))**2 + (mean(zwerte_q[:zl[0]])-mean(zwerte_q[zl[1]:zl[2]]))**2)
    yskal = 2448/math.sqrt((mean(xwerte_q[:zl[0]])-mean(xwerte_q[zl[3]:zl[4]]))**2 + (mean(ywerte_q[:zl[0]])-mean(ywerte_q[zl[3]:zl[4]]))**2 + (mean(zwerte_q[:zl[0]])-mean(zwerte_q[zl[3]:zl[4]]))**2)
    A = np.vstack([x_punkte, y_punkte, np.ones_like(x_punkte)]).T
    b = np.array(z_punkte)
    R = np.linalg.lstsq(A,b, rcond=-1)
    mat = R[0]
    
    #prüfen ob beliebige punkte in ebene liegen und ebene bilden
    x_neu = [-1000,1000,1000]
    y_neu = [-1000,1000,-1000]
    al = zip(x_neu,y_neu)

    #z_neu = [a[0]*mat[0] + a[1]*mat[1] + mat[2] for a in al]
    z_neu = [a[0]*mat[0] + a[1]*mat[1] for a in al] #mat[2] direkt =0, damit ebene im urpsrung liegt
    
    #skspatial
    plane_a = Plane.from_points(*np.vstack([x_neu,y_neu,z_neu]).T)
    
    plane_b = Plane.from_points([0,0,0],[1,1,0],[0,1,0])

    line_intersection = plane_a.intersect_plane(plane_b)
    gerade = line_intersection.direction/np.linalg.norm(line_intersection.direction) #gerade normieren


    winkel = math.acos(np.dot(plane_a.normal,plane_b.normal)/((np.linalg.norm(plane_a.normal)*np.linalg.norm(plane_b.normal))))
    winkel = winkel -math.pi
    print("drehwinkel_xy: ", winkel)
    n1 = gerade[0]
    n2 = gerade[1]
    s = math.sin(winkel)
    c = math.cos(winkel)
    drehmatrix = np.empty(shape=(3,3))
    drehmatrix[0] = [(n1**2)*(1-c)+c, n1*n2*(1-c), n2*s]	#n3 ist 0
    drehmatrix[1] = [n2*n1*(1-c), (n2**2)*(1-c)+c, -n1*s]
    drehmatrix[2] = [-n2*s, n1*s, c]

    list_zip_q = list(zip(xwerte_q, ywerte_q, zwerte_q))
    xd = [np.matmul(drehmatrix[0],np.array(p)) for p in list_zip_q] 
    yd = [np.matmul(drehmatrix[1],np.array(p)) for p in list_zip_q] 
    zd = [np.matmul(drehmatrix[2],np.array(p)) for p in list_zip_q]
    
    #Drehung um z-Achse vorbereitung
    werte_q = list(zip(xwerte_q, ywerte_q, zwerte_q))

    erste = [0]
    q_diff = [math.sqrt((f[0]-werte_q[c][0])**2 + (f[1]-werte_q[c][1])**2 + (f[2]-werte_q[c][2])**2) for c,f in enumerate(werte_q[1:])]
    q_diff = erste + q_diff


    #g-code
    file_g = open("kalibrationsfahrt.txt", 'r')
    xgcode = []
    ygcode = []
    zgcode = []
    file_gl = list(file_g)

    for l in file_gl[5:-4]: #erste 5 Zeilen überspringen
        l = l.split(' ')
        if l[2].startswith('P'):
            continue
        xgcode.append(float(l[2][1:]))
        ygcode.append(float(l[3][1:]))
        zgcode.append(float(l[4][1:]))

    file_g.close()
    gesch = int(file_gl[3].split(' ')[2][1:])
    gcode = list(zip(xgcode, ygcode, zgcode))



    for c,p in enumerate(q_diff):
        if p > 0.075:
            q_anf = c #erste bewegung
            break

    zeitpunkte = [] #punkte an denen neue linie beginnt
    zeitpunkte.append(q_anf)

    g_erste = [(0,0,0)] #startpunkt nicht immer hier
    gcode = g_erste + gcode




    for c,g in enumerate(gcode[1:-1]):
        dauer_v = freq * 60 * math.sqrt((g[0]-gcode[c][0])**2 + (g[1]-gcode[c][1])**2 + (g[2]-gcode[c][2])**2)/gesch
        dauer_nach = freq * 60* math.sqrt((g[0]-gcode[c+2][0])**2 + (g[1]-gcode[c+2][1])**2 + (g[2]-gcode[c+2][2])**2)/gesch
        #print(zeitpunkte[-1], dauer_v)
        von = int(zeitpunkte[-1] + dauer_v/2)
        
        bis = int(zeitpunkte[-1] + dauer_v + dauer_nach/2)
        zp = q_diff.index(min(q_diff[von:bis]))
        zeitpunkte.append(zp)

    #zeitpunkte.append(len(werte_q)) #nein, da sonst alle endpunkte die ausgleichsgerade beeinflussen
    for c,p in enumerate(q_diff[::-1]):
        if p > 0.075:
            q_end = len(q_diff) - c #erste bewegung
            break
    zeitpunkte.append(q_end)
    #print("Zeitpunkte", len(zeitpunkte), zeitpunkte, "Gcode", len(gcode), gcode)
    #Drehung um z-Achse ausührung
    list_zip_dreh = list(zip(xd, yd, zd))
    
    #gleiches mit regressionsgerade durch x probieren
    alpha_list = []
    #y_geraden = [(round(math.sin(math.radians(30*t)),6), round(math.cos(math.radians(30*t)),6)) for t in range(12)]
    y_geraden = [(1000,0),(0,1000)]
    rechts = 1
    for a,z in enumerate(zeitpunkte[:-1]):
        ende = zeitpunkte[a+1]
        A = np.vstack([xd[z+10:ende-10], np.ones_like(xd[z+10:ende-10])]).T
        b = np.array(yd[z+10:ende-10])
        R = np.linalg.lstsq(A,b, rcond=-1)
        mat = R[0]
        #print(mat)
        y_gerade = np.array(y_geraden[int(a/2)])
        #if a == 0 and mat[0] < 0:
            #rechts = -1
            
        r_gerade = np.array([1,mat[0]])
        alpha = math.acos(np.dot(y_gerade,r_gerade)/(np.linalg.norm(y_gerade)*np.linalg.norm(r_gerade)))
        if alpha >= math.pi/2:
            alpha = math.pi - alpha
        alpha_list.append(rechts*alpha)
        print("alpha: ",alpha, " geradengleichung: y = {} * x + {}".format(mat[0],mat[1]))
    
    #drehwinkel_z = mean(alpha_list)
    drehwinkel_z = mean(alpha_list[2:])
    drehwinkel_z_2 = mean(alpha_list[:2])
    #print('alpha_list',alpha_list)
    print('drehwinkel_z',drehwinkel_z, drehwinkel_z_2)
    drehmatrix_z = np.empty(shape=(3,3))
    drehmatrix_z[0] = [math.cos(drehwinkel_z), -math.sin(drehwinkel_z), 0]
    drehmatrix_z[1] = [math.sin(drehwinkel_z), math.cos(drehwinkel_z), 0]
    drehmatrix_z[2] = [0, 0, 1]
    
    xd = [np.matmul(drehmatrix_z[0],np.array(p)) for p in list_zip_dreh] 
    yd = [np.matmul(drehmatrix_z[1],np.array(p)) for p in list_zip_dreh] 
    zd = [np.matmul(drehmatrix_z[2],np.array(p)) for p in list_zip_dreh]
    
    #translation
    xoff_dreh = 0 -mean(xd[:q_anf-20])
    yoff_dreh = 0 -mean(yd[:q_anf-20])
    zoff_dreh = 0 -mean(zd[:q_anf-20])
    xlaenge = math.sqrt((mean(xwerte_q[:zl[0]])-mean(xwerte_q[zl[1]:zl[2]]))**2 + (mean(ywerte_q[:zl[0]])-mean(ywerte_q[zl[1]:zl[2]]))**2 + (mean(zwerte_q[:zl[0]])-mean(zwerte_q[zl[1]:zl[2]]))**2)
    ylaenge = math.sqrt((mean(xwerte_q[:zl[0]])-mean(xwerte_q[zl[3]:zl[4]]))**2 + (mean(ywerte_q[:zl[0]])-mean(ywerte_q[zl[3]:zl[4]]))**2 + (mean(zwerte_q[:zl[0]])-mean(zwerte_q[zl[3]:zl[4]]))**2)
    print("x laenge: ",xlaenge," y laenge: ",ylaenge)
    return(drehmatrix, drehmatrix_z, xoff_dreh, yoff_dreh, zoff_dreh, xskal, yskal)

def datei_schreiben(dateiname):
    file_q = open(dateiname, 'r')
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
    freq = int(1000000000 * len(file_ql)/(zeit_q[-1] - zeit_q[0]))
    
    matrix_ebene, matrix_z, xoff, yoff, zoff, xskali, yskali= koord_trans(xwerte_q, ywerte_q, zwerte_q, freq)
    '''
    file_k = open(file[:-4] + "_ergebniss_skaliert.txt", 'w')
    #file_k = open("kalibrationsdateien/" + time.strftime("%Y.%m.%d_%H.%M",time.gmtime()) +"_kalibration_ergebniss.txt", 'w')
    for l in range(3):
        file_k.write(str(matrix_ebene[l][0])+","+str(matrix_ebene[l][1])+","+str(matrix_ebene[l][2]) +'\n')
    for l in range(3):
        file_k.write(str(matrix_z[l][0])+","+str(matrix_z[l][1])+","+str(matrix_z[l][2]) +'\n')
    file_k.write(str(xoff)+","+str(yoff)+","+str(zoff)+"\n")
    file_k.write(str(xskali)+","+str(yskali)+"\n")
    file_k.close()
    '''
    print("Datei geschrieben: ",file[:-4] + "_ergebniss_skaliert.txt")
    
    

if __name__ == "__main__":
    print("Select Qualisys calibration file!")
    file = fd.askopenfilename(title='Qualisys-Daten auswählen',initialdir='D:\\FH Aachen\\Lernen\\Abschlussarbeiten\\Praxisprojekt\\Endergebnisse\\',multiple=False,filetypes=(('Kalibrationsdatei', '*.txt'), ('All files', '*.*')))

    
    datei_schreiben(file)
    
    #datei_schreiben("C:\\Users\\LAPTOP845_LGORISSEN\\Documents\\Qualisys\\python_neu\\python\\stepcraft\\ergebnisse\\2023.02.24_15.58_stern_6000.txt")
    
