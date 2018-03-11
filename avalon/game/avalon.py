configs = {
    5: [3, 2, [2, 3, 2, 3, 3],],
    6: [4, 2, [2, 3, 4, 3, 4],],
    7: [4, 3, [2, 3, 3, 4, 4],],
    8: [5, 3, [3, 4, 4, 5, 5],],
    9: [6, 3, [3, 4, 4, 5, 5],],
    10: [6, 4, [3, 4, 4, 5, 5],],
}


class AvalonGame(object):
    def __init__(self, num_players):
        self.num_players = num_players
        (self.num_resistance,
        self.num_spies,
        self.mission_sizes) = configs[num_players]