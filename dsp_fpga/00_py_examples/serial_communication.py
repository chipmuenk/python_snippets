# -*- coding: utf-8 -*-
"""
Created on Tue Sep 02 08:48:12 2014

@author: Michael W.
"""
#Informationen
#Das Fluke45 sendet bei eingeschaltetem Echo Mode den gesendeten Befehl zurück
#Jede gesendete Zeile des Messgerätes endet mit einem CR und LF
#CR = Carriage Return, LF = Line Feed

######################    
#       MACROS       #
######################


#mit Baud 9600 können übertragungen länger dauern, als die Prüfung auf einen
#gefüllten Eingangspuffer. In diesem Fall wird nichts empfangen. 
USE_BAUD_DELAY = False  






#######################
#       IMPORTS       #
#######################    
import serial
import sys
import struct
import time
import numpy as np



#==============================================================================

class Communicator(object):


    def openSerialPort(self, com):
        """
        serialPort öffnet den COM-Port zum Fluke mit den standard RS-232 Einstellungen
        
        Parameters
        ----------
        self
        """
    
        self.ser = serial.Serial(
                                 port=str(com),
                                 baudrate=9600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS,
                                 timeout = 1
                                 )
        self.ser.close()
        print("%s is open: %s" %(com, ("True" if self.ser.isOpen() else "False")))
                
        if(self.ser.isOpen() == False):
            print("COM ist nicht offen")
            try:
                self.ser.open()
                print("versuche COM zu oeffnen")
            except serial.SerialException:
                print("COM konnte nicht geoeffnet werden")
                self.settext("Ausgewaelter Port konnte nicht geoefnet werden")
    
    def serialScan(self):
        """
        Sucht nach verfügbaren Com-Ports und gibt diese in einer Liste zurück
        
        Parameters
        ----------
        self
        """
        
        ports = []
        for i in range(256):
            try:
                
    #Wenn der serielle Port NICHT geöfnet werden kann, wird eine Exception
    #"serial.SerialException" geschmissen. Diese wird abgefangen und die for-Schleife
    #läuft weiter OHNE dabei den nicht erreichbaren Port in die ports-Liste einzutragen            
                self.ser = serial.Serial(i)
                
    #Befülle dir Portliste mit den Com-Ports die geöfnet werden konnten
                ports.append([i, self.ser.portstr])
                self.ser.close()
            except serial.SerialException:
                pass
        print("COM-Ports:", ports)
        return ports
    
    
    
    
    
    ###############################################################################
    def serialReadLine(self):
        """
        serialReadLine liest alle gesendeten Zeilen des Fluke45 solange bis das
        Messgerät den Sendebetrieb einstellt. Der Sendebetrieb ist vorbei, sobald
        das Messgerät ein Steuerzeichen ('=>' oder '?>' oder '!>') gefolgt von einem
        CR und LF (CR = Carriage Return, LF = Line Feed)
        
        Parameters
        ----------
        self
        """
        Value = []
        i=0
        while (i == 0):
            if (self.ser.inWaiting > 0):
                
                #Lese die nächste Zeile und füge die an die Liste "Value"
                #hinten an
                Value.append(self.ser.readline())
            
            #Ist das "Macro" USE_BAUD_DELAY True, dann lasse dir Zeit beim
            #überprüfen des Inputbuffers. 
            elif(USE_BAUD_DELAY):  
                
                #Da die Baud 9600 sehr langsam ist, muss gewartet werden ob 
                #doch etwas im Eingangspuffer liegt
                time.sleep(0.0625)   
                if (self.ser.inWaiting > 0):
                    
                    #Lese die nächste Zeile und füge die an die Liste "Value"
                    #hinten an
                    Value.append(self.ser.readline())
    
            #Prüfe ob das letzte Element in der "Value" Liste ein vom Fluke45
            #gesendetes Steuerzeichen ist.        
            if (Value != 0):
                
                #"=>\r\n" Steuerzeichen für Befehl verstanden, ausgeführt
                #und bereit für einen neuen Befehl
                if (Value[-1] == "=>\r\n"):
           
                    i = 1
                    self.Debug_Msg("Fluke45 hat Befehl verstanden u. ausgefuehrt")
                #"?>\r\n" Steuerzeichen für Befehlsfehler
                #Befehl wurde nicht verstanden.
                elif (Value[-1] == '?>\r\n'):
                    i = 2
                    self.Debug_Msg("Befehl wurde vom Fluke45 nicht verstanden!")
                #!>\r\n Steuerzeichen für Syntaxfehler
                # Befehl wurde verstanden doch ist nicht ausführbar
                # Siehe Fluke45 Handbuch Seite 5-5!
                elif (Value[-1] == '!>\r\n'):
                    i = 3
                    self.Debug_Msg("Befehl verstanden, aber vom Fluke45 nicht ausfuehrbar")
                
        return Value
    
                                       
                 
    ###############################################################################        
    def serialSend(self, SendMsg):
        """
        SerialSend sendet den übergebenen SendMsg-String an das Messgerät und
        ruft anschließend die Funktion serialReadLine auf, um die Antwort des
        Messgerätes zu erhalten.
        Die Antwort des Messgerätes wird z.Z. nur auf der Console und dem
        Textbrouser dargestellt.
        
        Parameters
        ---------        
        Self : 
        
        SendMsg : Der String der an das Messgerät gesendet werden soll.
        
        ReturnValue : None
        
        """
#        self.ser.write(SendMsg) # only Py2?
#        self.ser.write(bytes(SendMsg.encode('ascii'))) # Py3
        pass
#        self.ser.write(bytes(SendMsg.encode())) # Py3

    def serial_send_bytes(self, send_int):
        """
        Send the integer send_int as two bytes 
        
        Parameters
        ---------         
        
        send_int : the integer to be sent
        
        Returns : None
        
        """
#        self.ser.write(SendMsg) # only Py2?
#        self.ser.write(bytes(SendMsg.encode('ascii'))) # Py3

        

        send_bytes = struct.pack("<H", send_int) # unsigned short, little endian
        print(send_bytes)
        self.ser.write(str(send_bytes))   
         
    def closePort(self):
        """
        exitApp schließt die Serieleschnitstelle und beendet anschließend das
        Programm
        
        Parameters
        ----------
        self
        """
        if(self.ser.isOpen() == True):
            self.ser.close()
    
    def generate_sine(self):
        self.x = np.arange(100)
        self.y = np.round(1 + np.sin(2 * np.pi * self.x / 100)*2**13).astype(np.int16)
        for i in range(100):
            print("%d \t %d" %(self.x[i], self.y[i]))       
            
                
    def Selbsttest(self):
        self.serialSend("*TST?\n")
    
if __name__ == '__main__':
    
    my_com = Communicator()
    ports = my_com.serialScan()
    my_com.generate_sine()
    my_com.openSerialPort(ports[0][1])
    print(my_com.ser.isOpen())
    print("\nStart Transmission\n")
    i = 0
    while True:
        sin_str = str(my_com.y[i%100])
        sin_int = my_com.y[i%100]
        print(sin_str, sin_int)
        my_com.serial_send_bytes(sin_int)
        i += 1
        time.sleep(0.1)
    
    print("finished")