gross_mass = {}
inert_mass = {}
propellant_mass = {}
ISP = {}
thrust = {}
burntime= {}

booster_count = 4

gross_mass["boosters"] = 43772*4
gross_mass["stage1"] = 245900
gross_mass["stage2"] = 37130
gross_mass["stage3"] = 12310
gross_mass["GTO"] = 4723
gross_mass["satellite_str"] = 1270

inert_mass["boosters"] = 4493*4
inert_mass["stage1"] = 17900
inert_mass["stage2"] = 3625
inert_mass["stage3"] = 1570

for _type in ["boosters", "stage1", "stage2", "stage3"]:
	propellant_mass[_type] = gross_mass[_type] - inert_mass[_type]

mass = {}
mass["boosters"] = sum(gross_mass.values())-gross_mass["boosters"]
mass["stage1"] = mass["boosters"] - gross_mass["stage1"]
mass["stage2"] = mass["stage1"] - gross_mass["stage2"]
mass["stage3"] = mass["stage2"] - gross_mass["stage3"]

ISP["boosters"] = 278
ISP["stage1"] = 278
ISP["stage2"] = 296
ISP["stage3"] = 446

thrust["liftoff"] = 5440000
thrust["boosters"] = 752003
thrust["stage1"] = 3034100
thrust["stage2"] = 720965
thrust["stage3"] = 62703

burntime["boosters"] = 142
burntime["stage1"] = 205
burntime["stage2"] = 129
burntime["stage3"] = 781

stages = ["stage1", "stage2", "stage3"]

events = {}

_events = {}
_events[16 - 6] = "end of vertical ascent"
_events[2*60 + 30 - 6] = "booster ejection"
_events[3*60 + 31 - 6] = "first stage seperation"
_events[3*60 + 34 - 6] = "second stage ignition"
_events[4*60 + 24 - 6] = "fairing ejection"
_events[5*60 + 43 - 6] = "second stage seperation"
_events[5*60 + 48 - 6] = "third stage ignition"
_events[18*60 + 49 - 6] = "third stage end"
_events[20*60 + 56 - 6] = "satellite separation"

for i, name in enumerate(sorted(_events.keys())):
	events[str(i) + _events[name]] = name
	
perigee = 225000
apogee = 35945
