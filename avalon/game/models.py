from django.db import models
from django.contrib.auth.models import AbstractUser


class AvalonUser(AbstractUser):
    def __repr__(self):
        return '<AvalonUser user: {u}>'.format(u=self.username)

class AvalonGame(models.Model):
    user = models.ForeignKey(AvalonUser, related_name='user')
    quest_master = models.ForeignKey('AvalonGameUser',
        related_name='quest_master',
        blank=True,
        null=True)
    current_quest = models.ForeignKey('AvalonQuest',
        related_name='current_quest',
        blank=True,
        null=True)

    def __repr__(self):
        return '<AvalonGame users: {u}>'.format(
            u=self.users.values_list('username', flat=True))

    @property
    def users(self):
        user_ids = AvalonGameUser.objects.filter(game=self
            ).values_list('user_id', flat=True)
        return AvalonUser.objects.filter(pk__in=user_ids)

    @property
    def game_users(self):
        return AvalonGameUser.objects.filter(game=self)

    @property
    def quests(self):
        ordered_quests = []
        current_quest = self.current_quest
        while current_quest is not None:
            ordered_quests.append(current_quest)
            current_quest = current_quest.next_quest

        return ordered_quests

    def who_is(self, role):
        return self.game_users.filter(role=role)

    def create(cls, new_game):
        avalon_game = cls(user=new_game.user)
        avalon_game.save()

        # KW: TODO refactor this out for creating quests
        quests = [
            AvalonQuest.objects.create(game=avalon_game, num_players=n)
            for n
            in new_game.quest_sizes]

        for i, quest in enumerate(quests):
            if i == 0:
                avalon_game.current_quest = quest
                avalon_game.save()
                quest.next_quest = quests[i + 1]
            elif i == len(quests) -1 :
                quest.prev_quest = quests[i - 1]
            else:
                quest.prev_quest = quests[i - 1]
                quest.next_quest = quests[i + 1]

            quest.save()

        # KW: TODO refactor this out for linking ordered game users
        users = [x[0] for x in new_game.users]
        for user, role in new_game.users:
            current_player = AvalonGameUser.objects.create(
                game=avalon_game,
                user=user,
                role=role)

        for index in range(len(users)):
            prev = self.game_users.filter(user=users[(index - 1) % len(users)])
            curr = self.game_users.filter(user=users[index])
            nex = self.game_users.filter(user=users[(index + 1) % len(users)])

            prev.next_player = curr
            curr.prev_player = prev
            curr.next_player = nex
            nex.prev_player = curr

            prev.save()
            curr.save()
            nex.save()

        # KWL: TODO ask for age so we always start with youngest xP
        avalon_game.quest_master = curr
        avalon_game.save()

        return avalon_game

class AvalonQuest(models.Model):
    game = models.ForeignKey(AvalonGame)
    num_players = models.IntegerField(default=2)

    prev_quest = models.ForeignKey('AvalonQuest',
        related_name='prev',
        blank=True,
        null=True)
    next_quest = models.ForeignKey('AvalonQuest',
        related_name='next',
        blank=True,
        null=True)

    def __repr__(self):
        return '<AvalonQuest game: {g}, num_players: {n}>'.format(
            g=self.game.pk,
            n=self.num_players)

    @property
    def is_successful(self):
        return all(AvalonQuestMember.objects.filter(quest=self
            ).values_list('vote_pass', flat=True))

    def reset_quest_members(self, game_users):
        assert len(game_users) == self.num_players, 'quest size is incorrect'
        # KW: TODO persist previous tries
        AvalonQuestMember.objects.filter(quest=self).delete()

        for user in game_users:
            AvalonQuestMember.objects.create(quest=self, member=user)

        return

class AvalonGameUser(models.Model):
    LOYAL_SERVANT = 1
    MINION_OF_MORDRED = 2
    ASSASIN = 3
    MERLIN = 4
    MORGANA = 5
    MORDRED = 6
    PERCIVAL = 7

    GAME_ROLES = (
        (LOYAL_SERVANT, LOYAL_SERVANT),
        (MINION_OF_MORDRED, MINION_OF_MORDRED),
        (ASSASIN, ASSASIN),
        (MERLIN, MERLIN),
        (MORGANA, MORGANA),
        (MORDRED, MORDRED),
        (PERCIVAL, PERCIVAL),
    )

    user = models.ForeignKey(AvalonUser)
    game = models.ForeignKey(AvalonGame)

    prev_player = models.ForeignKey('AvalonGameUser',
        related_name='prev',
        blank=True,
        null=True)
    next_player = models.ForeignKey('AvalonGameUser',
        related_name='next',
        blank=True,
        null=True)

    role = models.CharField(
        max_length=3,
        choices=GAME_ROLES,
        default=LOYAL_SERVANT)

    def __repr__(self):
        return '<AvalonGameUser game: {g}, user: {u}>'.format(
            g=self.game.pk,
            u=self.user.username)

class AvalonQuestMember(models.Model):
    quest = models.ForeignKey(AvalonQuest)
    member = models.ForeignKey(AvalonGameUser)
    vote_pass = models.BooleanField(default=True)


