from django.db import models
from django.contrib.auth.models import AbstractUser

from game.exceptions import QuestSizeIncorrect


class AvalonUser(AbstractUser):
    pass

class AvalonGame(models.Model):
    user = models.ForeignKey(AvalonUser, related_name='user')
    quest_master = models.ForeignKey('AvalonGameUser',
        related_name='quest_master',
        blank=True,
        null=True)
    first_quest = models.ForeignKey('AvalonQuest',
        related_name='first_quest',
        blank=True,
        null=True)
    current_quest = models.ForeignKey('AvalonQuest',
        related_name='current_quest',
        blank=True,
        null=True)

    @property
    def users(self):
        return [gu.user for gu in self.ordered_game_users]

    @property
    def ordered_game_users(self):
        first_game_user = AvalonGameUser.objects.get(game=self, user=self.user)
        ordered_users = [first_game_user]

        current_game_user = first_game_user.next_player
        while current_game_user is not None and current_game_user != first_game_user:
            ordered_users.append(current_game_user)
            current_game_user = current_game_user.next_player

        return ordered_users

    @property
    def game_users(self):
        return AvalonGameUser.objects.filter(game=self)

    @property
    def quests(self):
        ordered_quests = []

        current_quest = self.first_quest
        for _ in range(5):
            ordered_quests.append(current_quest)
            current_quest = current_quest.next_quest

        return ordered_quests

    def finalize_quest(self):
        self.current_quest = self.current_quest.next_quest
        self.quest_master = self.quest_master.next_player
        self.save()

        return

    def handle_vote_for_quest(self, user, vote):
        quest_user = AvalonGameUser.objects.get(game=self, user=user)
        quest_user.vote_for_quest(vote)

        return

    def finalize_vote_for_quests(self):
        if not self.current_quest.is_approved:
            self.quest_master = self.quest_master.next_player
            self.save()

        return

    def handle_vote_on_quest(self, user, vote):
        # KW: TODO there should be validation that user here is on the quest
        quest_user = AvalonGameUser.objects.get(game=self, user=user)
        quest_member = AvalonQuestMember.objects.get(
            quest=self.current_quest,
            member=quest_user)

        quest_member.vote = vote
        quest_member.save()

        return

    def who_is(self, role):
        return self.game_users.filter(role=role)

    def create(cls, new_game):
        avalon_game = cls(user=new_game.user)
        avalon_game.save()

        # KW: TODO refactor this out for linking ordered game users
        users = [x[0] for x in new_game.users]
        for user, role in new_game.users:
            AvalonGameUser.objects.create(
                game=avalon_game,
                user=user,
                role=role)

        for index in range(len(users)):
            prev = avalon_game.game_users.get(user=users[(index - 1) % len(users)])
            curr = avalon_game.game_users.get(user=users[index])
            nex = avalon_game.game_users.get(user=users[(index + 1) % len(users)])

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

        # KW: TODO refactor this out for creating quests
        quests = [
            AvalonQuest.objects.create(game=avalon_game, num_players=n)
            for n
            in new_game.quest_sizes]

        for i, quest in enumerate(quests):
            if i == 0:
                avalon_game.current_quest = avalon_game.first_quest = quest
                avalon_game.save()
                quest.next_quest = quests[i + 1]
                quest.prev_quest = quests[i - 1]
            elif i == len(quests) -1 :
                quest.next_quest = quests[0]
                quest.prev_quest = quests[i - 1]
            else:
                quest.next_quest = quests[i + 1]
                quest.prev_quest = quests[i - 1]

            quest.save()

            for game_user in AvalonGameUser.objects.filter(game=avalon_game):
                AvalonQuestVote.objects.get_or_create(
                    quest=quest,
                    game_user=game_user)

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

    @property
    def votes_for_quest(self):
        game_users = self.game.game_users
        quest_votes = AvalonQuestVote.objects.filter(
            quest=self,
            game_user__in=game_users)
        return quest_votes.values_list('game_user__user__username', 'vote')

    @property
    def votes_on_quest(self):
        return self.members.values_list('member__user__username', 'vote')

    @property
    def is_approved(self):
        votes_for_quest =self.votes_for_quest
        if (len(votes_for_quest)) == 0:
            return False

        approval_votes = len([vote for _, vote in votes_for_quest if vote ])
        denial_votes = len([vote for _, vote in votes_for_quest if not vote ])

        return (approval_votes / len(votes_for_quest)) > 0.5

    @property
    def is_successful(self):
        return all([vote for username, vote in self.votes_on_quest])

    @property
    def status(self):
        pass

    @property
    def members(self):
        return AvalonQuestMember.objects.filter(quest=self)

    def reset_members(self, game_user_ids):
        if len(game_user_ids) != self.num_players:
            raise QuestSizeIncorrect

        AvalonQuestMember.objects.filter(quest=self).delete()

        for user_id in game_user_ids:
            AvalonQuestMember.objects.create(quest=self, member_id=user_id)

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
        (LOYAL_SERVANT, 'LOYAL_SERVANT'),
        (MINION_OF_MORDRED, 'MINION_OF_MORDRED'),
        (ASSASIN, 'ASSASIN'),
        (MERLIN, 'MERLIN'),
        (MORGANA, 'MORGANA'),
        (MORDRED, 'MORDRED'),
        (PERCIVAL, 'PERCIVAL'),
    )

    user = models.ForeignKey(AvalonUser)
    game = models.ForeignKey(AvalonGame, blank=True, null=True)

    prev_player = models.ForeignKey('AvalonGameUser',
        related_name='prev',
        blank=True,
        null=True)
    next_player = models.ForeignKey('AvalonGameUser',
        related_name='next',
        blank=True,
        null=True)

    role = models.IntegerField(
        choices=GAME_ROLES,
        default=LOYAL_SERVANT)

    @property
    def game_role(self):
        return [u[1] for u in self.GAME_ROLES if u[0] == self.role][0]

    @property
    def special_knowledge(self):
        VISIBLE_MINIONS = [
            self.MINION_OF_MORDRED,
            self.ASSASIN,
            self.MORGANA,
        ]
        MINIONS_OF_MORDRED = VISIBLE_MINIONS + [self.MORDRED]
        PERCIVALS_DUO = [self.MERLIN, self.MORGANA]

        game_users = AvalonGameUser.objects.filter(game=self.game).exclude(role=self.role)
        if self.role in MINIONS_OF_MORDRED:
            return game_users.filter(role__in=MINIONS_OF_MORDRED)
        elif self.role == self.MERLIN:
            return game_users.filter(role__in=VISIBLE_MINIONS)
        elif self.role == self.PERCIVAL:
            return game_users.filter(role__in=PERCIVALS_DUO)

        return game_users.filter(role=0)

    def vote_for_quest(self, vote):
        quest_vote, created = AvalonQuestVote.objects.get_or_create(
            quest=self.game.current_quest,
            game_user=self)

        quest_vote.vote = vote
        quest_vote.save()

        return

class AvalonQuestMember(models.Model):
    quest = models.ForeignKey(AvalonQuest)
    member = models.ForeignKey(AvalonGameUser)
    vote = models.BooleanField(default=True)

class AvalonQuestVote(models.Model):
    """
    whether or note a game_user voted yes or no on a group to go on a quest
    """
    quest = models.ForeignKey(AvalonQuest)
    game_user = models.ForeignKey(AvalonGameUser)
    vote = models.BooleanField(default=False)