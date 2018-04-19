from consts import *
from data import *
import math
import matplotlib.pyplot as plt


def timperiod(perigee_alt, apogee_alt):
	a = (perigee_alt + apogee_alt)/2.0 + r_e
	return (4*(pi**2)*(a**3)/mu)**0.5
	
def velocity(hp, ha, perigee=False):
	h = (2* mu * (hp+r_e) * (ha+r_e)/ (hp + ha + 2*r_e))**0.5
	if(perigee):
		return h/(hp+r_e)
	else:
		return h/(ha+r_e)

def beta(_type):
	return (gross_mass[_type]-inert_mass[_type])/burntime[_type]

def g(height):
	return go/((1+(height/r_e))**2)
	
def printParams(event):
	global X
	global H
	global V
	global M
	global G
	global q_o
	global Theta
	print(event)
	print("X: " + str(X[-1]))
	print("H: " + str(H[-1]))
	print("V: " + str(V[-1]))
	print("M: " + str(M[-1]))
	print("G: " + str(G[-1]))
	print("qo: "+ str(qo))
	print("Theta: "+str(Theta[-1]))

thrust_liftoff = 5440000

time = [i for i in xrange(20*60+56+1)]

event_list = sorted(events.keys())

V = [0.0]
M = [float(sum(gross_mass.values()))]
#M = [486000.0]
H = [0.0]
X = [0.0]

G = [go]

Theta_o = 1.2*pi/180.0
Theta = [Theta_o]
propellant_mass_2 = propellant_mass

for t in time[1:]:
	if t <= events["0end of vertical ascent"]:
		_beta = (beta("boosters") + beta("stage1"))
		M.append(M[-1]- _beta)
		propellant_mass_2["boosters"] = propellant_mass_2["boosters"] - beta("boosters")
		propellant_mass_2["stage1"] = propellant_mass_2["stage1"] - beta("stage1")
		_V = (M[-1]/M[0])
		V.append(-1*go*ISP["boosters"]*math.log(_V)-G[-1]*t)
		H.append( (M[0]*go*ISP["boosters"]/_beta)* (_V*math.log(_V)+(1-_V)) - 0.5*G[-1]*(t**2))
		G.append(g(H[-1]))
		X.append(0)
		if(t == events["0end of vertical ascent"]):
			#qo = G[-1] * math.sin(Theta_o)/V[-1]
			qo = 1.283*(10**-3)
			printParams("\n\n>====end of vertical ascent")
			Mo = M[-1]
			To = t
			Ho = H[-1]
	elif t <= events["1booster ejection"]:
		Theta.append(Theta[-1]+qo)
		H.append(G[-1]/(4*(qo**2))*(	math.cos(2*Theta[0]) - math.cos(2*Theta[-1])) + Ho )
		X.append(G[-1]/(2*(qo**2))*( Theta[-1]-Theta[0]- 1/2.0*(math.sin(2*Theta[-1])-math.sin(2*Theta[0]))))
		M.append(Mo* (math.e**(-2*G[-1]/(qo*go*ISP["boosters"]) * (math.sin(Theta[-1]) - math.sin(Theta[0]) ))) )
		V.append(G[-1]*math.sin(Theta[-1])/ qo)
		G.append(g(H[-1]))
		if(t == events["1booster ejection"]):
			M[-1] = M[-1] - inert_mass["boosters"]
			printParams("\n\n>====booster ejection")
			M1 = M[-1]
			T1 = t
			H1 = H[-1]
			X1 = X[-1]
			Theta_1 = Theta[-1]
		#pass

	elif t <= events["2first stage seperation"]:
		
		Theta.append(Theta[-1]+qo)
		H.append(G[-1]/(4*(qo**2))*(math.cos(2*Theta_1) - math.cos(2*Theta[-1])) + H1 )
		X.append(G[-1]/(2*(qo**2))*( Theta[-1]-Theta_1- 1/2.0*(math.sin(2*Theta[-1])-math.sin(2*Theta_1))) + X1 )
		M.append(M1* (math.e**(-2*G[-1]/(qo*go*ISP["stage1"]) * (math.sin(Theta[-1]) - math.sin(Theta_1) ))) )
		V.append(G[-1]*math.sin(Theta[-1])/ qo)
		G.append(g(H[-1]))
		
		if(t == events["2first stage seperation"]):
			#print(M[-1]) - inert_mass["stage1"]
			#M[-1] = M[0] - gross_mass["boosters"] - gross_mass["stage1"]
			M[-1] = M[-1] - inert_mass["stage1"]
			printParams("\n\n>====first stage seperation")
			M3 = M[-1]
			T3 = t
			H3 = H[-1]
			X3 = X[-1]
			Theta_3 = Theta[-1]
			
	#elif t <= events['3second stage ignition']:	
	#elif t <= events['4fairing ejection']:
	elif(t <= events['5second stage seperation']):
		Theta.append(Theta[-1]+qo)
		H.append(G[-1]/(4*(qo**2))*(math.cos(2*Theta_3) - math.cos(2*Theta[-1])) + H3 )
		X.append(G[-1]/(2*(qo**2))*( Theta[-1]-Theta_3- 1/2.0*(math.sin(2*Theta[-1])-math.sin(2*Theta_3))) + X3 )
		M.append(M3* (math.e**(-2*G[-1]/(qo*go*ISP["stage2"]) * (math.sin(Theta[-1]) - math.sin(Theta_3) ))) )
		V.append(G[-1]*math.sin(Theta[-1])/ qo)
		G.append(g(H[-1]))
		
		if(t == events["5second stage seperation"]):
			#M[-1] = M[0] - gross_mass["boosters"] - gross_mass["stage1"] - gross_mass["stage2"]
			M[-1] = M[-1] - inert_mass["stage2"]
			printParams("\n\n>====5second stage seperation")
			M4 = M[-1]
			T4 = t
			H4 = H[-1]
			X4 = X[-1]
			Theta_4 = Theta[-1]
	#elif t <= events['6third stage ignition']:
	#	pass
	elif t <= events['7third stage end']:
		Theta.append(Theta[-1]+qo)
		H.append(G[-1]/(4*(qo**2))*(math.cos(2*Theta_4) - math.cos(2*Theta[-1])) + H4 )
		X.append(G[-1]/(2*(qo**2))*( Theta[-1]-Theta_4- 1/2.0*(math.sin(2*Theta[-1])-math.sin(2*Theta_4))) + X4 )
		M.append(M4* (math.e**(-2*G[-1]/(qo*go*ISP["stage2"]) * (math.sin(Theta[-1]) - math.sin(Theta_4) ))) )
		V.append(G[-1]*math.sin(Theta[-1])/ qo)
		G.append(g(H[-1]))
		
		if(t == events["7third stage end"]):
			printParams("\n\n>====7third stage end")
			M[-1] = M[-1] - inert_mass["stage3"]
plt.plot(X, H)
plt.savefig("H_X.png")
plt.close()

plt.plot(time[:len(M)], M)
plt.savefig("M.png")
plt.close()

plt.plot(time[:len(V)], V)
plt.savefig("V.png")
plt.close()

plt.plot([i*180/pi for i in Theta])
plt.savefig("Theta.png")
plt.close()
