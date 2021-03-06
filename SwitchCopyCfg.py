#!/usr/bin/env python3
#################################################
#   Remote download of switches configuration   #
#          wersion 1.10 28.03.2018r.            #
#   For switches not connected to Radius        #
#################################################

import os
import time
import pexpect
from datetime import datetime

sciezka = "/opt/magazyn/pliki_serwis/"
sciez_log = sciezka + "LOGI/TFTP/"
sciez_dane_gl = sciezka + "SIEC/"
kat_cel = ""

#********************************************#
#        List of supported switches          #
#********************************************#
LISTA = [
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
	["<adres ip>", "<nazwa switcha>", "<hasło>"],
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

def rem_kom(adres, host, sciez_log, kat_cel, haslo):
	child = pexpect.spawnu("telnet "+adres)
	child.logfile = open(sciez_log+log_nazwa(adres), "w")
	child.expect(".*assword:")
	child.send(haslo+"\r")
	child.expect(".*>")
	child.send("en\r")
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

#  Main

n = 0
while n < len(LISTA):
	adres = LISTA[n][0] 
	host  = LISTA[n][1] 
	haslo = LISTA[n][2]
	rem_kom(adres, host, sciez_log, kat_cel, haslo)
	n += 1
	time.sleep( 1 )



