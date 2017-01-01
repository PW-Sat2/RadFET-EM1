import time
from serial import Serial

dev = Serial('/dev/ttyS22', 4800)

s = dev.readline().strip()

start = time.time()

first = True

vMOSFirst = [0, 0, 0]
vDiodeFirst = 0

while True:
	s = dev.readline().strip()
	
	if first:
		start = time.time()

	now = time.time()
	diff = now-start

	print "time = ", diff
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
	
	print "mos = ", mos, "diode = ", diode
	print "dDiode = ", dDiode
	print "dTemp = ", dTemp

	print "shift prediction = ", dMosShiftPrediction
	
	print "corrected = ", MosVth0
	
	print "\n\n"