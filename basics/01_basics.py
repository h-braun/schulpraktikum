heinrich_name = "Heinrich Braun"
heinrich_alter = 28
heinrich_groesse = 1.85
heinrich_ist_schueler = False

thomas_name = "Thomas Ehrenreich"
thomas_ist_schueler = True

philipp_name = "Philipp Ketzberg"
thomas_ist_schueler = False

namens_liste = [heinrich_name, thomas_name, philipp_name]

for name in namens_liste:
    print(name)

if heinrich_ist_schueler:
    print("Heinrich geht noch zur Schule")
else:
    print("Heinrich ist kein Schüler mehr")


if thomas_ist_schueler:
    print("Thomas geht noch zur Schule")
else:
    print("Thomas ist kein Schüler mehr")
