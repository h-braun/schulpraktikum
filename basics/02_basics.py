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


heinrich = Person("Heinrich Braun", alter=28, groesse=1.87)
thomas = Person("Thomas Ehrenreich", ist_schueler=True)
philipp = Person("Philipp Ketzberg")


heinrich.geht_zur_schule()
thomas.geht_zur_schule()
