import random

from game.roles import (
    Assasin,
    LoyalServant,
    Merlin,
    MinionOfMordred,
    Mordred,
    Morgana,
    Percival,
)

class AvalonGame(object):
    # KW: TODO figure out roles per num players
    BASE_ROLES = ['merlin', 'assasin']

    CONFIGS = {
        5   : [3, 2, [2, 3, 2, 3, 3], BASE_ROLES],
        6   : [4, 2, [2, 3, 4, 3, 4], BASE_ROLES],
        7   : [4, 3, [2, 3, 3, 4, 4], BASE_ROLES],
        8   : [5, 3, [3, 4, 4, 5, 5], BASE_ROLES],
        9   : [6, 3, [3, 4, 4, 5, 5], BASE_ROLES],
        10  : [6, 4, [3, 4, 4, 5, 5], BASE_ROLES],
    }

    def __init__(self, users):
        self._setup_game_configs(users)

        self._create_empty_roles()
        self._distribute_roles(users)

        return

    def _create_empty_roles(self):
        self.assasin = Assasin()
        self.merlin = Merlin()
        self.mordred = Mordred()
        self.morgana = Morgana()
        self.percival = Percival()

        self.loyal_1 = LoyalServant()
        self.loyal_2 = LoyalServant()
        self.loyal_3 = LoyalServant()
        self.loyal_4 = LoyalServant()

        self.minion_1 = MinionOfMordred()
        self.minion_2 = MinionOfMordred()
        self.minion_3 = MinionOfMordred()
        self.minion_4 = MinionOfMordred()

        return

    def _setup_game_configs(self, users):
        self.users = users
        self.current_mission = 0

        (self.num_resistance,
        self.num_spies,
        self.mission_sizes,
        self.roles) = self.CONFIGS[len(users)]

        return

    def _distribute_roles(self, users):
        random.shuffle(users)

        index = 0
        for role in self.roles:
            getattr(self, role).set_player(users[index])
            index += 1

        return

    def vote_to_go_on_quest(self):
        pass

    def print_debug_text(self):
        debug_fields = [
            'users',
            'num_resistance',
            'num_spies',
            'mission_sizes',
            'current_mission',
            'roles',

            'break',
            'assasin',
            'merlin',
            'mordred',
            'morgana',
            'percival',

            'break',
            'loyal_1',
            'loyal_2',
            'loyal_3',
            'loyal_4',

            'break',
            'minion_1',
            'minion_2',
            'minion_3',
            'minion_4',
        ]

        debug_text = ''
        for field_name in debug_fields:
            if field_name == 'break':
                debug_text += '<br><br><br>'
            else:
                key = field_name
                value = getattr(self, field_name)
                debug_text += '{key}: {value}<br>'.format(key=key, value=str(value))

        return debug_text