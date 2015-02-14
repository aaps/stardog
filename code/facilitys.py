
class Facility(object):
    def __init__(self, planet):
        self.planet = planet

    def update(self):
        pass


class Shop(Facility):
    def __init__(self, planet):
        Facility.__init__(self, planet)
    # getClosesedsystem(Facility)
    # getClosesedUniverse(Facility)
    # getaveragesystem(item)
    # getmaxsystem(item)
    # getminsystem(item)
    # getaverageuniverse(item)
    # getmaxuniverse(item)
    # getminuniverse(item)
    # getaveragerepairsystem
    # getmaxrepairsystem
    # getminrepairsystem
    # getclosessystem(item)
    # getclosesuniverse(item)


class Fitter(Facility):
    # a list of parts and the fitting efficiency that makes
    # up the price of fitting something
    # * the weight / fitters in the neighborhood
    def __init__(self, planet):
        Facility.__init__(self, planet)


class ShopAndFitt(Shop, Fitter):
    def __init__(self, planet):
        Shop.__init__(self, planet)
        Fitter.__init__(self, planet)


class Smelter(Facility):
    def __init__(self, planet):
        Facility.__init__(self, planet)
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
    def __init__(self, planet):
        Facility.__init__(self, planet)
    # get all the sell/buy prices in the facinity of this trade terminal
    # player reserve a good on the list you want to buy sell
    # (you are on the mission)


class Repair(Facility):
    def __init__(self, planet):
        Facility.__init__(self, planet)
    # update
    # find materials to repair with
    # repair
    # a button for player, perhaps a button that will repair a module
    # the price will be dependable on repair efficiency
    # and the amount of repair shops in the neighborhood
