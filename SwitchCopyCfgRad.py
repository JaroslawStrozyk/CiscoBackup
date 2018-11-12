#!/usr/bin/env python3
#################################################
#   remote download of switches configuration   #
#           wersion 1.00 12.11.2016r.           #
#   For switches  connected to Radius           #
#################################################

import os
import time
import pexpect
from datetime import datetime

sciezka = "/opt/magazyn/pliki_serwis/"
sciez_log = sciezka + "LOGI/TFTP/"
sciez_dane_gl = sciezka + "TFTP/"
kat_cel = ""

#********************************************#
#        List of supported switches          #
#********************************************#
LISTA = [
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
	["<adres ip>", "<nazwa switch-a>",    "<uzytkownik>", "<hasło>"],
]



def kat_nazwa(sciez_dane_gl):
	gkat = datetime.now().strftime('%Y-%m-%d')
	sciez = sciez_dane_gl + gkat
	if not os.path.exists(sciez):
		os.makedirs(sciez)
		os.chmod(sciez,0o777)
	return gkat

def log_nazwa(adres):
	adres = adres+"_"+datetime.now().strftime('%Y-%m-%d_%H:%M')+".log"
	return adres

def arch_kom(host, kat_cel):
    adr = "<adres ip>"
	komenda = "copy startup-config tftp://"+adr+"/"+kat_cel+"/"+host+"_"+datetime.now().strftime('%Y-%m-%d')+".cfg"
	return komenda

def rem_kom(adres, host, sciez_log, kat_cel, uzyt, haslo):
	child = pexpect.spawnu("telnet "+adres)
	child.logfile = open(sciez_log+log_nazwa(adres), "w")
	child.expect(".*sername:")
	child.send(uzyt+"\r")	
	child.expect(".*assword:")
	child.send(haslo+"\r")
	child.expect(".*#")
	child.sendline(arch_kom(host, kat_cel)+"\r")
	child.expect(".*]?")
	child.send("\r")
	child.expect(".*]?")
	child.send("\r")
	child.expect(".*#")
	child.send("exit\r")

kat_cel = kat_nazwa(sciez_dane_gl)
sciez_dane = sciez_dane_gl + kat_cel

# Main

n = 0
while n < len(LISTA):
	adres = LISTA[n][0] 
	host  = LISTA[n][1]
	uzyt  = LISTA[n][2]
	haslo = LISTA[n][3]
	rem_kom(adres, host, sciez_log, kat_cel, uzyt, haslo)
	n += 1
	time.sleep( 1 )



