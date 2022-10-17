class Person:
    def __init__(self, name, alter=0, groesse=0.0, ist_schueler=False):
        self.name = name
        self.alter = alter
        self.groesse = groesse
        self.ist_schueler = ist_schueler

    def geht_zur_schule(self):
        if self.ist_schueler:
            print(f"{self.name} geht noch zur Schule.")
        else:
            print(f"{self.name} ist kein Schüler mehr.")


class Schulklasse:
    def __init__(self, schueler_liste, klassenzimmer=301):
        self.schueler = schueler_liste
        self.klassenzimmer = klassenzimmer

    def neuer_schueler(self, schueler):
        if schueler.ist_schueler:
            self.schueler.append(schueler)
        else:
            print(f"{schueler.name} ist kein Schüler mehr.")


heinrich = Person("Heinrich Braun", alter=28, groesse=1.87)
thomas = Person("Thomas Ehrenreich", ist_schueler=True)
philipp = Person("Philipp Ketzberg")
