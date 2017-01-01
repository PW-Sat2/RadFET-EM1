import time
from serial import Serial

#dev = Serial('/dev/ttyS22', 4800)
#
#s = dev.readline().strip()

first = True

vMOSFirst = [0, 0, 0]
vDiodeFirst = 0

a = open("data.txt", "r")

for s in a:
	s = s.strip()
	
	lsb = [eval(i) for i in s.split(" ")]
	uv = [i * 2.5e6 / 2**24 for i in lsb]
	
	mos = uv[0:3]
	diode = uv[3]
	
	if first:
		first = False
		vMOSFirst = mos
		vDiodeFirst = diode
	
	
	dTempCoeff = -2045 # uV/deg C
	dDiode = diode - vDiodeFirst
	dTemp = dDiode/dTempCoeff
	
	
	dMosVthCoeff = -100 # uV/deg C
	
	dMosShiftPrediction = dMosVthCoeff*dTemp
	MosVth0 = [i - dMosShiftPrediction for i in mos]
	
	print " ".join([str(i) for i in mos]), dMosShiftPrediction
	#print "mos = ", mos, "diode = ", diode
	#print "dDiode = ", dDiode
	#print "dTemp = ", dTemp
    #
	#print "shift prediction = ", dMosShiftPrediction
	#
	#print "corrected = ", MosVth0
	#
	#print "\n\n"