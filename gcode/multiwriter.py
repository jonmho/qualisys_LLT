import os.path
import math

art_l = ['s','ex', 'ey', 'e']
art = input("s:    Stern\nex:    Ebene X\ney:    Ebene Y\ne:    Ebene\n")
while art not in art_l:
    print("Ungültige Eingabe")
    art = input("s:    Stern\nex:    Ebene X\ney:    Ebene Y\ne:    Ebene\n")
    
geschw = int(input("Geschwindigkeit? 0-12000mm/s\n"))
while geschw <= 0 or geschw > 12000:
    print("Ungültige Geschwindigkeit!")
    geschw = int(input("Geschwindigkeit? 0-12000mm/s\n"))
    
hoehe = float(input("Höhe? -145mm bis 0mm\n"))
while hoehe <-145 or hoehe >0:
    print("Ungültige Höhe!")
    hoehe = float(input("Höhe? -145mm bis 0mm\n"))

if art == 's':
    laenge = float(input("Armlänge angeben! maximal 611mm\n"))
    while laenge < 0 or laenge >611:
        print("Ungültige Länge!")
        laenge = float(input("Armlänge angeben! maximal 611mm\n"))

durchgaenge = int(input("Anzahl der Durchgänge angeben!\n"))
        
name = input("Dateinamen eingeben! \n")
folder = "U:\\Praxisprojekt\\stepcraft\\cnc_gcode\\"
dname = folder + name + ".txt"

if os.path.isfile(dname):
    print("Dateiname existiert bereits!")
    name2 = input("Anderen Namen eingeben oder mit Enter überschreiben!")
    if name2 == "":
        dname = folder + name + ".txt"
    else:
        dname = folder + name2 + ".txt"

#stern
if art == 's':
    with open(dname , 'w') as f:
        counter = 0
        f.write("%{}\n".format(name))
        for durch in range(durchgaenge):
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G28.1\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G90 G1 F6000 X611 Y1222 Z{}\n".format(hoehe))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F{}\n".format(geschw))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P3000\n")
            
            for t in range(12):
                x = round(611 + laenge * math.sin(math.radians(30*t)),6)
                y = round(1222 + laenge * math.cos(math.radians(30*t)),6)
                z = round(hoehe,6)
                n0 = "N{:0>4} ".format(counter)
                f.write(n0 + "G1 X{} Y{} Z{}\n".format(x,y,z))
                counter += 10
                n0 = "N{:0>4} ".format(counter)
                f.write(n0 + "G1 X611 Y1222 Z{}\n".format(hoehe))
                counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P3000\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F6000 X5 Y5 Z-5\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "G28.1\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "M30")
        
#ebene_x
elif art == 'ex':
    with open(dname , 'w') as f:
        counter = 0
        f.write("%{}\n".format(name))
        for durch in range(durchgaenge):
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G28.1\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G90 G1 F6000 X0 Y0 Z{}\n".format(hoehe))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F{}\n".format(geschw))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P3000\n")
        
            for t in range(27):
                n0 = "N{:0>4} ".format(counter)
                z = hoehe
                if t%4 == 0:
                    x = 1222
                    y = (t * 94)
                elif t%4 == 1:
                    x = 1222
                    y = (t * 94 + 94)
                elif t%4 == 2:
                    x = 0
                    y = (t * 94)
                elif t%4 == 3:
                    x = 0
                    y = (t * 94 + 94)    
                f.write(n0 + "G1 X{} Y{} Z{}\n".format(x,y,z))
                counter += 10
                
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P3000\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F6000 X5 Y5 Z-5\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "G28.1\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "M30")

#ebene_y
elif art == 'ey':
    with open(dname , 'w') as f:
        counter = 0
        f.write("%{}\n".format(name))
        for durch in range(durchgaenge):
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G28.1\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G90 G1 F6000 X0 Y0 Z{}\n".format(hoehe))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F{}\n".format(geschw))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P3000\n")
        
            for t in range(27):
                n0 = "N{:0>4} ".format(counter)
                z = hoehe
                if t%4 == 0:
                    x = t*47
                    y = 2444
                elif t%4 == 1:
                    x = t*47 + 47
                    y = 2444
                elif t%4 == 2:
                    x = t*47
                    y = 0
                elif t%4 == 3:
                    x = t*47+47
                    y = 0
                    
                f.write(n0 + "G1 X{} Y{} Z{}\n".format(x,y,z))
                counter += 10
                
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P3000\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F6000 X5 Y5 Z-5\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "G28.1\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "M30")
        
elif art == 'e':
    with open(dname , 'w') as f:
        counter = 0
        f.write("%{}\n".format(name))
        for durch in range(durchgaenge):
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G28.1\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G90 G1 F6000 X611 Y1222 Z{}\n".format(hoehe))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F{}\n".format(geschw))
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P3000\n")
        
            for t in range(52):
                n0 = "N{:0>4} ".format(counter)
                z = hoehe
                t1 = int(t/4)
                if t%4 == 0:
                    x = 611 + 47 * (1+t1)
                    y = 1222 + 94 * t1
                elif t%4 == 1:
                    x = 611 + 47 * (1+t1)
                    y = 1222 - 94 * (1+t1)
                elif t%4 == 2:
                    x = 611 - 47 * (1+t1)
                    y = 1222 - 94 * (1+t1)
                elif t%4 == 3:
                    x = 611 - 47 * (1+t1)
                    y = 1222 + 94 * (1+t1)
                    
                f.write(n0 + "G1 X{} Y{} Z{}\n".format(x,y,z))
                counter += 10
            #letzes stück
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 X1222 Y2444 Z{}\n".format(hoehe))
            counter += 10 
            
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P2000\n")
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F6000 X5 Y5 Z-5\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "G28.1\n")
        counter += 10
        n0 = "N{:0>4} ".format(counter)
        f.write(n0 + "M30")
