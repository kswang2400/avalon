import random

from game.models import AvalonGame, AvalonGameUser, AvalonUser
from game.roles import (
    Assasin,
    LoyalServant,
    Merlin,
    MinionOfMordred,
    Mordred,
    Morgana,
    Percival,
)

# KW: TODO figure out roles per num players (default: 6)
# KW: TODO don't hardcode loyal/minions in base roles
# BASE_ROLES = ['merlin', 'assasin']
BASE_ROLES = [
    AvalonGameUser.MERLIN,
    AvalonGameUser.ASSASIN,
    AvalonGameUser.LOYAL_SERVANT,
    AvalonGameUser.LOYAL_SERVANT,
    AvalonGameUser.LOYAL_SERVANT,
    AvalonGameUser.MINION_OF_MORDRED,
]
CONFIGS = {
    5   : [3, 2, [2, 3, 2, 3, 3], BASE_ROLES],
    6   : [4, 2, [2, 3, 4, 3, 4], BASE_ROLES],
    7   : [4, 3, [2, 3, 3, 4, 4], BASE_ROLES],
    8   : [5, 3, [3, 4, 4, 5, 5], BASE_ROLES],
    9   : [6, 3, [3, 4, 4, 5, 5], BASE_ROLES],
    10  : [6, 4, [3, 4, 4, 5, 5], BASE_ROLES],
}

class Game(object):
    def __init__(self, pk=None, users=None):
        if pk:
            try:
                self.game = SavedGame(pk)
            except AvalonGame.DoesNotExist:
                self.game = NewGame(
                    users=list(AvalonUser.objects.filter(username__in=[
                        'kevin',
                        'evan',
                        'choi',
                        'kent',
                        'marcus',
                        'greg',
                    ])))
        else:
            self.game = NewGame(users)


    def get_debug_context(self):
        debug_fields = [
            'users',
            'quest_sizes',
            'current_quest',

            # 'assasin',
            # 'merlin',
            # 'mordred',
            # 'morgana',
            # 'percival',
        ]

        debug_context = {}
        for field_name in debug_fields:
            key = field_name
            value = getattr(self.game, field_name)
            debug_context[key] = value

        return debug_context

class SavedGame(object):
    def __init__(self, pk):
        saved_game = AvalonGame.objects.get(pk=pk)

        self.avalon_game = saved_game
        self.current_quest = saved_game.current_quest
        self.users = saved_game.users

        (self.num_resistance,
        self.num_spies,
        self.quest_sizes,
        self.roles) = CONFIGS[len(self.users)]

        # self.assasin = saved_game.assasin
        # self.merlin = saved_game.merlin
        # self.mordred = saved_game.mordred
        # self.morgana = saved_game.morgana
        # self.percival = saved_game.percival

class NewGame(object):
    def __init__(self, users):
        self._create_empty_roles()

        roles = self._setup_game_configs(users)
        ordered_users_with_roles = self._distribute_roles(users, roles)

        self.users = ordered_users_with_roles
        self.avalon_game = AvalonGame.create(AvalonGame, self)

        return

    def _create_empty_roles(self):
        self.assasin = Assasin()
        self.merlin = Merlin()
        self.mordred = Mordred()
        self.morgana = Morgana()
        self.percival = Percival()

        return

    def _setup_game_configs(self, users):
        self.user = users[0]
        self.users = users
        self.current_quest = 1

        (self.num_resistance,
        self.num_spies,
        self.quest_sizes,
        self.roles) = CONFIGS[len(users)]

        return self.roles

    def _distribute_roles(self, users, roles):
        random.shuffle(users)
        random.shuffle(roles)

        return list(zip(users, roles))