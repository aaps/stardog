# facillitys.py

from adjectives import PARTS


class Company(object):
    def __init__(self,planet):
        self.planet = planet
        self.facilitys = []
        self.name = "dummy Company"
        self.cash = 1000

    def addFacility(self, facility):
        facility.company = self
        self.facilitys.append(facility)

    def update(self):
        for facility in self.facilitys:
            facility.update()


class Facility(object):
    def __init__(self):
        self.name = "dummy Facility"
        self.suply = []
        self.needs = {}
        self.company = None

    def update(self):
        pass


class Shop(Facility):
    def __init__(self,):
        Facility.__init__(self)


class Fitter(Facility):
    # a list of parts and the fitting efficiency that makes
    # up the price of fitting something
    # * the weight / fitters in the neighborhood
    def __init__(self):
        Facility.__init__(self)


class ShopAndFitt(Shop, Fitter):
    def __init__(self, company):
        Shop.__init__(self)
        Fitter.__init__(self)


class Smelter(Facility):
    def __init__(self):
        Facility.__init__(self)
    # update
    # look if there is ore of scrap on planet or in a
    # shop on planet and get / buy it, if the price is right
    # also make metal bars and sell them to a shop that is perhaps on planet.
    # update trade terminals

    # sell
    # something for player

    # buy
    # something for player or other ai ?


class TradeTerminal(Facility):
    def __init__(self):
        Facility.__init__(self)
    # get all the sell/buy prices in the facinity of this trade terminal
    # player reserve a good on the list you want to buy sell



class Repair(Facility):
    def __init__(self):
        Facility.__init__(self)
    # update
    # find materials to repair with
    # repair
    # a button for player, perhaps a button that will repair a module
    # the price will be dependable on repair efficiency
    # and the amount of repair shops in the neighborhood
