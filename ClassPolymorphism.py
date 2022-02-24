
#Parent Class:
class Person:
    age = 30
    sex = "F"
    height = None
    
    #method to return properties
    def stats(self):
        msg = "\nAge: {}\nSex: {}\nHeight: {}".format(self.age, self.sex, self.height)
        return msg

#child class 1
class Citizen(Person):
    #two new properties
    nationality = "British"
    party = "Whig"

    #polymorphism: stats() now returns nationality and party
    def stats(self):
        msg = "\nAge: {}\nNationality: {}\nParty: {}".format(self.age, self.nationality, self.party)
        return msg
    
#child class 2
class Tourist(Person):
    visit_duration = "1 week"
    passport_issuer = "Sweden"

    #polymorphism: stats() now returns visit duration and passport issuer.
    def stats(self):
        msg = "\nAge: {}\nPassport Issuer: {}\nVisit Duration: {}".format(self.age, self.passport_issuer, self.visit_duration)
        return msg
    

if __name__ == "__main__":

#print data for each instance to demonstrate differentiation.
    sami = Person()
    print(sami.stats())

    ken = Citizen()
    print(ken.stats())

    bruh = Tourist()
    print(bruh.stats())
