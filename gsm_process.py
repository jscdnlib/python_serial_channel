#Importieren der noetigen Module
from time import sleep
import RPi.GPIO as GPIO
import serial, re
#Benennen der PINS
Tuer1 = 7
Tuer2 = 11
Tuer3 = 13
Tuer4 = 15
Tuer5 = 12
Tuer6 = 16
RFID = 23  
KBesetzt1 = 18
KBesetzt2 = 22
KBesetzt3 = 24
KBesetzt4 = 26
KBesetzt5 = 19
KBesetzt6 = 21
#Festlegen der Ein und Ausgaenge
GPIO.setmode(GPIO.BOARD)
GPIO.setup(KBesetzt1, GPIO.IN)
GPIO.setup(KBesetzt2, GPIO.IN)
GPIO.setup(KBesetzt3, GPIO.IN)
GPIO.setup(KBesetzt4, GPIO.IN)
GPIO.setup(KBesetzt5, GPIO.IN)
GPIO.setup(KBesetzt6, GPIO.IN)
GPIO.setup(RFID, GPIO.IN)
GPIO.setup(Tuer1, GPIO.OUT)
GPIO.setup(Tuer2, GPIO.OUT)
GPIO.setup(Tuer3, GPIO.OUT)
GPIO.setup(Tuer4, GPIO.OUT)
GPIO.setup(Tuer5, GPIO.OUT)
GPIO.setup(Tuer6, GPIO.OUT)
GPIO.output(Tuer1, GPIO.LOW)
GPIO.output(Tuer2, GPIO.LOW)
GPIO.output(Tuer3, GPIO.LOW)
GPIO.output(Tuer4, GPIO.LOW)
GPIO.output(Tuer5, GPIO.LOW)
GPIO.output(Tuer6, GPIO.LOW)
#Definitionen
speicher = [0,0,0,0,0,0]
pin = 0
number = 0
listpin = 0
belegt1 = 0
belegt2 = 0
belegt3 = 0
belegt4 = 0
belegt5 = 0
belegt6 = 0
#Abfrage ob Eingabe richtig
def is_pin_valid(pin):
	return len(pin) == 4 and pin.isdigit()
#Funktion VOLL
def voll():
	voll = 0 in speicher
	return voll
#Beschreiben der Liste			
def Liste(listpin):
	gefunden = 0
	beschrieben = 0
	print(pin)
	for k in range(6):
		if speicher[k] == listpin:
			speicher[k] = 0
			gefunden = True
			print(speicher)
			break
	if voll() == False:
		print "Voll"
	for j in range(6):
		if speicher[j] == 0 and not gefunden:
			speicher[j] = listpin
			print(speicher)
			break
	Beschaltung(listpin)
#Abruf eines Anrufs
def Anruf():
	korrekt = 0
	#serielle Schnittstellen Einstellungen
	command_channel = serial.Serial(
        	port='/dev/ttyUSB0',
        	baudrate=115200,
        	parity=serial.PARITY_NONE,
        	stopbits=serial.STOPBITS_ONE,
        	bytesize=serial.EIGHTBITS
	)
	#serielle Schnittstellen verbindung wird geoeffnet
	command_channel.open()
	#Aktivirung der Anrufer ID
	command_channel.write("AT+CLIP=1" + "\r\n")
	#serielle Schnittstellen verbindung wird geschlossen
	command_channel.close()
	#serielle Schnittstelle Einstellungen
	ser = serial.Serial(
        	port='/dev/ttyUSB2',
        	baudrate=9600,
        	parity=serial.PARITY_NONE,
        	stopbits=serial.STOPBITS_ONE,
        	bytesize=serial.EIGHTBITS
	)
	#serielle Schnittstellen verbindung wird geoeffnet
	ser.open()
	#Anrufer ID wird ausgelesen
	pattern = re.compile('.*CLIP.*"\+([0-9]+)",.*')
	while 1:
        	buffer = ser.read(ser.inWaiting()).strip()
        	buffer = buffer.replace("\n","")
        	match = pattern.match(buffer)
        	if match:
			number = match.group(1)
                	#verifizirung der Anrufer ID
                	if number in open('userid.txt').read():
                		print "User found"
				print(number)
				listpin = number
				Liste(listpin)
				break
                	else:
                		print "User not found"
				print(number)
				break
#Pineingabe                	
def Pin():
	for versuch in range(1,6):
		pin = raw_input("Bitte geben sie ihren Pin ein")
		print(pin)
		data = open("pin.txt").read()
		if pin in data and is_pin_valid(pin):
			listpin = pin
			Liste(listpin)
			break	
		else:
			print "Falsche Eingabe"
			continue
	if versuch > 4:
		print "5 Fehlversuche"
		sleep(2)			
#Auswahl zwischen Pineingabe und Anruf
def Auswahl():
	print "Bitte Taste 1 fuer einen Anruf"
	print "Oder Taste 2 fuer eine Pin Eingabe"
	auswahl = 0
	auswahl = raw_input("Auswahl")
	if auswahl == "1":
		Anruf()
	if auswahl == "2":
		Pin()
#Beschaltung der GPIOs	
def Beschaltung(listpin):
	print(listpin)
	print(speicher)
	#Kabine 1	
	if GPIO.input(KBesetzt1) == False and speicher[0] == listpin or GPIO.input(KBesetzt1) == True and speicher[0] == "0":
		GPIO.output(Tuer1, GPIO.HIGH)
		sleep(5)
		GPIO.output(Tuer1, GPIO.LOW)
		sleep(4)
		if GPIO.input(KBesetzt1) == False and listpin == speicher[0]:
			print "Kein Fahrrad in Kabine 1 erkannt"
			speicher[0] = 0
	#Kabine 2
	elif GPIO.input(KBesetzt2) == False and speicher[1] == listpin or GPIO.input(KBesetzt2) == True and speicher[1] == "0":
                GPIO.output(Tuer2, GPIO.HIGH)
                sleep(5)
                GPIO.output(Tuer2, GPIO.LOW)
		sleep(4)
                if GPIO.input(KBesetzt2) == False and listpin == speicher[1]:
                        print "Kein Fahrrad in Kabine 2 erkannt"
			speicher[1] = 0


	#Kabine 3	
	elif GPIO.input(KBesetzt3) == False and speicher[2] == listpin or GPIO.input(KBesetzt3) == True and speicher[2] == "0":
		GPIO.output(Tuer3, GPIO.HIGH)
                sleep(5)
                GPIO.output(Tuer3, GPIO.LOW)
                sleep(4)
                if GPIO.input(KBesetzt3) == False and listpin == speicher[2]:
                        print "Kein Fahrrad in Kabine 3 erkannt"
			speicher[2] = 0
	#Kabine 4
	elif GPIO.input(KBesetzt4) == False and speicher[3] == listpin or GPIO.input(KBesetzt4) == True and speicher[3] == "0":
                GPIO.output(Tuer4, GPIO.HIGH)
                sleep(5)
                GPIO.output(Tuer4, GPIO.LOW)
                sleep(4)
                if GPIO.input(KBesetzt4) == False and listpin == speicher[3]:
                        print "Kein Fahrrad in Kabine 4 erkannt"
			speicher[3] = 0
	#Kabine 5
	elif GPIO.input(KBesetzt5) == False and speicher[4] == listpin or GPIO.input(KBesetzt5) == True and speicher[4] == "0":
                GPIO.output(Tuer5, GPIO.HIGH)
                sleep(5)
                GPIO.output(Tuer5, GPIO.LOW)
                sleep(4)
                if GPIO.input(KBesetzt5) == False and listpin == speicher[4]:
                        print "Kein Fahrrad in Kabine 5 erkannt"
			speicher[4] = 0
	#Kabine 6
	elif GPIO.input(KBesetzt6) == False and speicher[5] == listpin or GPIO.input(KBesetzt6) == True and speicher[5] == "0":
                GPIO.output(Tuer6, GPIO.HIGH)
                sleep(5)
                GPIO.output(Tuer6, GPIO.LOW)
                sleep(4)
                if GPIO.input(KBesetzt6) == False and listpin == speicher[5]:
                        print "Kein Fahrrad in Kabine 6 erkannt"
			speicher[5] = 0
	#Abfrage eines Fehlers
	else:
		print "Fehler"
#Hauptprogram	
def main():
	while True:
		Auswahl()


if __name__ == "__main__":
	main()
