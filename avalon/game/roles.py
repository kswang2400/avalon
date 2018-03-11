class AvalonRole(object):
    def __init__(self, player=None):
        self.player = player

    def set_player(self, user):
        self.player = user
    
    def __str__(self):
        return '<[{r}: {p}]>'.format(
            r=self.__class__.__name__,
            p=self.player)


class LoyalServant(AvalonRole):
    def __init__(self):
        super(LoyalServant, self).__init__()

class MinionOfMordred(AvalonRole):
    def __init__(self):
        super(MinionOfMordred, self).__init__()


class Assasin(MinionOfMordred):
    def __init__(self):
        super(Assasin, self).__init__()

class Merlin(LoyalServant):
    def __init__(self):
        super(Merlin, self).__init__()

class Mordred(MinionOfMordred):
    def __init__(self):
        super(Mordred, self).__init__()

class Morgana(MinionOfMordred):
    def __init__(self):
        super(Morgana, self).__init__()

class Percival(LoyalServant):
    def __init__(self):
        super(Percival, self).__init__()