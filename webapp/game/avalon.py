import random

from game import roles
from game.models import AvalonGame, AvalonGameUser, AvalonUser, AvalonQuest


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
        self.game = SavedGame(pk) if pk else NewGame(users)

    def get_debug_context(self, debug=False):
        debug_fields = [
            'pk',
            'users',
            'quest_sizes',
            'first_quest',
            'current_quest',

            'assasin',
            'merlin',
            'mordred',
            'morgana',
            'percival',

            'loyal_servants',
            'minions_of_mordred',

            'quests',
            'quest_master',
            'game_users',
        ]

        debug_context = {
            'debug': debug,
        }
        for field_name in debug_fields:
            key = field_name
            value = getattr(self.game, field_name)
            debug_context[key] = value

        return debug_context

    def mock_game_user_quest_member_votes(self):
        for game_user in self.game.game_users:
            game_user.vote_for_quest(bool(random.randint(0, 1)))

        return

class SavedGame(object):
    def __init__(self, pk):
        saved_game = AvalonGame.objects.get(pk=pk)

        self.avalon_game = saved_game
        self.pk = saved_game.pk
        self.first_quest = saved_game.first_quest
        self.current_quest = saved_game.current_quest
        self.users = saved_game.users

        (self.num_resistance,
        self.num_spies,
        self.quest_sizes,
        self.roles) = CONFIGS[len(self.users)]

        self.assasin = saved_game.who_is(AvalonGameUser.ASSASIN)
        self.merlin = saved_game.who_is(AvalonGameUser.MERLIN)
        self.mordred = saved_game.who_is(AvalonGameUser.MORDRED)
        self.morgana = saved_game.who_is(AvalonGameUser.MORGANA)
        self.percival = saved_game.who_is(AvalonGameUser.PERCIVAL)

        self.loyal_servants = saved_game.who_is(AvalonGameUser.LOYAL_SERVANT)
        self.minions_of_mordred = saved_game.who_is(AvalonGameUser.MINION_OF_MORDRED)

        self.quests = self.avalon_game.quests
        self.quest_master = self.avalon_game.quest_master
        self.game_users = self.avalon_game.game_users

class NewGame(object):
    def __init__(self, users):
        self._create_empty_roles()

        roles = self._setup_game_configs(users)
        ordered_users_with_roles = self._distribute_roles(users, roles)

        self.users = ordered_users_with_roles

        self.avalon_game = AvalonGame.create(AvalonGame, self)

        # KW: TODO make this cleaner
        self.pk = self.avalon_game.pk
        self.quests = self.avalon_game.quests
        self.quest_master = self.avalon_game.quest_master
        self.game_users = self.avalon_game.game_users
        self.first_quest = self.avalon_game.first_quest

        return

    def _create_empty_roles(self):
        self.assasin = roles.Assasin()
        self.merlin = roles.Merlin()
        self.mordred = roles.Mordred()
        self.morgana = roles.Morgana()
        self.percival = roles.Percival()

        return

    def _setup_game_configs(self, users):
        self.user = users[0]
        self.users = users
        self.current_quest = 1 # KW: this is wrong, this needs to be a db object

        (self.num_resistance,
        self.num_spies,
        self.quest_sizes,
        self.roles) = CONFIGS[len(users)]

        return self.roles

    def _distribute_roles(self, users, roles):
        random.shuffle(list(users))
        random.shuffle(list(roles))

        ordered_users_with_roles = list(zip(users, roles))

        # KW: TODO its time to define game interface for saved/new game
        # KW: TODO this is the wrong place for this
        # KW: also new created games use AvalonUser because AvalonGameUser not yet created
        self.loyal_servants = [
            x[0]
            for x
            in ordered_users_with_roles
                if x[1] == AvalonGameUser.LOYAL_SERVANT]

        self.minions_of_mordred = [
            x[0]
            for x
            in ordered_users_with_roles
                if x[1] == AvalonGameUser.MINION_OF_MORDRED]

        return ordered_users_with_roles