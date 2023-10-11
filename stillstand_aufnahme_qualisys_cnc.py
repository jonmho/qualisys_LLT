import qtm
import asyncio
import time
import threading
from statistics import mean
from tkinter import filedialog as fd
import tkinter as tk
import numpy as np

#new measurement and close really necessary? beide rauskommentiert line50... und line68
def between_callback():
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(qualisys_task.start_qualisys())
    loop.close()
    
class Qualisys_stream():
    
    def __init__(self, dname, file_kal):
        self.zeit_0 = None
        self.aktiv = False
        #kalibrationdatei auslesen
        '''
        kal = open(file_kal, 'r')
        kal_list = []
        for i in list(kal):
            kal_list.append([float(k) for k in i.split(',')])
        self.drehmatrix_ebene = np.array([kal_list[0], kal_list[1], kal_list[2]])
        self.drehmatrix_z = np.array([kal_list[3], kal_list[4], kal_list[5]])
        self.translate = np.array(kal_list[6])
        '''
        #dname = input("Enter filename!\n")
        filename = "ergebnisse/" + time.strftime("%Y.%m.%d_%H.%M",time.gmtime()) + "_{}.txt".format(dname)
        self.f = open(filename, 'w')
        self.counter = 0
        self.faktor = int(input("Nur jeden x-ten Wert nehmen. x: "))
    
    def stop_qualisys(self):
        self.aktiv = False
               
    def on_packet(self, packet):
        """ Callback function that is called everytime a data packet arrives from QTM """
 
        header, markers = packet.get_6d_residual()
        robot = markers[0][0]
        if self.counter%self.faktor == 0:
            #werte=np.array([robot.x, robot.y, robot.z])
            #werte_e = np.matmul(self.drehmatrix_ebene, werte)
            #werte_d = np.matmul(self.drehmatrix_z, werte_e)
            #xwert,ywert,zwert = werte_d+self.translate
            xwert,ywert,zwert = np.array([robot.x, robot.y, robot.z])
            self.f.write(str(xwert) + "," + str(ywert) + "," + str(zwert) + "," + str(time.perf_counter_ns()) + "\n")
            #self.f.write(str(robot[0].x) + "," + str(robot[0].y) + "," + str(robot[0].z) + "," + str(time.perf_counter_ns()) + "\n")
        self.counter += 1
           
    async def start_qualisys(self):
        connection = await qtm.connect("127.0.0.1") #connect to host pc from host pc
            
        if connection is None:
            print("no connection")
            return  

            
        print("stream started")
        self.aktiv = True
        
        while self.aktiv:
            await connection.stream_frames(components=["6dres"], on_packet=self.on_packet)  
        #close connection and file
        
        self.f.close()

if __name__ == "__main__":
    dateiname = input("Enter filename!\n")
    dauer = input("Laufzeit eingeben!\n")
    #root = tk.Tk()
    #print("Kalibrationsdatei auswählen!")
    #file_kal = fd.askopenfilename(title='Kalibrationsdatei auswählen',initialdir='C:\\Users\\LAPTOP845_LGORISSEN\\Documents\\Qualisys\\python_neu\\python\\stepcraft\\kalibrationsdateien',filetypes=(('Kalibrationsdatei', '*.txt'), ('All files', '*.*')))
    file_kal = None
    #root.destroy()
    qualisys_task = Qualisys_stream(dateiname, file_kal)
    p1 = threading.Thread(target=between_callback, args=())
    input("Press Enter to start measurement!\n")
    p1.start()
    if dauer == "":
        input("Press Enter again to stop measurement! \n")
    else:
        dauer = int(dauer)
        time.sleep(dauer)
    qualisys_task.stop_qualisys()
    print("Measurement finished")


