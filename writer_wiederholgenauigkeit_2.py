import os.path

durchgaenge = int(input("Anzahl der Durchgänge angeben!\n"))

x,y,z = [float(i) for i in input("X Y Z eingeben, mit Leerzeichen trennen!\n").split(" ")]
while x <0 or x > 1222 or y < 0 or y > 2444 or z != 0:
    print("Ungültige Werte eingegeben! 0<x<1222 0<y<2444 0<z<0")
    x,y,z = [float(i) for i in input("X Y Z eingeben, mit Leerzeichen trennen!\n").split(" ")]
geschw = int(input("Geschwindigkeit? 0-12000mm/s\n"))
while geschw <= 0 or geschw > 12000:
    print("Ungültige Geschwindigkeit!")
    geschw = int(input("Geschwindigkeit? 0-12000mm/s\n"))
    
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

with open(dname , 'w') as f:
    counter = 0
    f.write("%{}\n".format(name))#
    #anfang
    counter += 10
    n0 = "N{:0>4} ".format(counter)
    f.write(n0 + "G28.1\n")
    counter += 10
    n0 = "N{:0>4} ".format(counter)
    f.write(n0 + "G90 G1 F8000 X{} Y{} Z{}\n".format(x,y,z))
    counter += 10
    n0 = "N{:0>4} ".format(counter)
    f.write(n0 + "G1 F{}\n".format(geschw))
    counter += 10   
    n0 = "N{:0>4} ".format(counter)
    f.write(n0 + "G04 P2000\n")
    #mittelteil
    punkte = [(0,0,-145),(435,0,0),(0,435,0),(435,0,-145),(435,435,0),(0,435,-145),(435,435,-145)]
    for p in punkte[1:3]:
        for durch in range(durchgaenge):
            for c in range(1,4):
                counter += 10
                n0 = "N{:0>4} ".format(counter)
                f.write(n0 + "G1 X{} Y{} Z{}\n".format(c*p[0]/3, c*p[1]/3, c*p[2]/3))
                counter += 10   
                n0 = "N{:0>4} ".format(counter)
                f.write(n0 + "G04 P2000\n")
                
            counter += 10
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G1 F8000 X0 Y0 Z0\n")
            counter += 10   
            n0 = "N{:0>4} ".format(counter)
            f.write(n0 + "G04 P2000\n")
        
    #ende
    counter += 10
    n0 = "N{:0>4} ".format(counter)
    f.write(n0 + "M30")