import random

from game.models import AvalonGame
from game.roles import (
    Assasin,
    LoyalServant,
    Merlin,
    MinionOfMordred,
    Mordred,
    Morgana,
    Percival,
)

class Game(object):
    def __init__(self, pk=None, users=None):
        if pk:
            self.game = SavedGame(pk)
        else:
            self.game = NewGame(users)

class SavedGame(object):
    def __init__(self, pk):
        saved_game = AvalonGame.objects.get(pk=pk)

class NewGame(object):
    # KW: TODO figure out roles per num players (default: 6)
    # KW: TODO don't hardcode loyal/minions in base roles
    # BASE_ROLES = ['merlin', 'assasin']
    BASE_ROLES = [
        'merlin',
        'assasin',
        'loyal_1',
        'loyal_2',
        'loyal_3',
        'minion_1',
    ]

    CONFIGS = {
        5   : [3, 2, [2, 3, 2, 3, 3], BASE_ROLES],
        6   : [4, 2, [2, 3, 4, 3, 4], BASE_ROLES],
        7   : [4, 3, [2, 3, 3, 4, 4], BASE_ROLES],
        8   : [5, 3, [3, 4, 4, 5, 5], BASE_ROLES],
        9   : [6, 3, [3, 4, 4, 5, 5], BASE_ROLES],
        10  : [6, 4, [3, 4, 4, 5, 5], BASE_ROLES],
    }

    def __init__(self, users):
        self._create_empty_roles()

        roles = self._setup_game_configs(users)
        self._distribute_roles(users, roles)

        # self.save_game_data()

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
        self.user = users[0]
        self.users = users
        self.current_quest = 0

        (self.num_resistance,
        self.num_spies,
        self.quest_sizes,
        self.roles) = self.CONFIGS[len(users)]

        return self.roles

    def _distribute_roles(self, users, roles):
        random.shuffle(users)

        index = 0
        for role in roles:
            getattr(self, role).set_player(users[index])
            index += 1

        return

    def save_game_data(self):
        print('\n\nsave game data\n\n')
        game = AvalonGame.create(self)

        return

    def get_table_configs(self):
        return {
            'user': self.user,
        }

    def vote_to_go_on_quest(self):
        pass

    def get_debug_context(self):
        debug_fields = [
            'users',
            'quest_sizes',
            'current_quest',

            'assasin',
            'merlin',
            # 'mordred',
            # 'morgana',
            # 'percival',

            'loyal_1',
            'loyal_2',
            'loyal_3',
            # 'loyal_4',

            'minion_1',
            # 'minion_2',
            # 'minion_3',
            # 'minion_4',
        ]

        debug_context = {}
        for field_name in debug_fields:
            key = field_name
            value = getattr(self, field_name)
            debug_context[key] = value

        return debug_context