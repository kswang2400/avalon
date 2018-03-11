from django.db import models
from django.contrib.auth.models import AbstractUser


class AvalonUser(AbstractUser):
    def __repr__(self):
        return '<AvalonUser user: {u}>'.format(u=self.username)

class AvalonGame(models.Model):
    QUEST_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    user = models.ForeignKey(AvalonUser, related_name='user')
    quest_master = models.ForeignKey('AvalonGameUser', related_name='quest_master', blank=True, null=True)
    current_quest = models.CharField(
        max_length=1,
        choices=QUEST_CHOICES,
        default='1')

    def __repr__(self):
        return '<AvalonGame users: {u}>'.format(u=self.users.values_list('username', flat=True))

    @property
    def users(self):
        user_ids = AvalonGameUser.objects.filter(game=self).values_list('user_id', flat=True)
        return AvalonUser.objects.filter(pk__in=user_ids)

    @property
    def game_users(self):
        return AvalonGameUser.objects.filter(game=self)

    def create(cls, new_game):
        avalon_game = cls(
            user=new_game.user,
            current_quest=new_game.current_quest,
        )
        avalon_game.save()

        # KW: TODO refactor this out for linking ordered game users
        users = [x[0] for x in new_game.users]
        for user, role in new_game.users:
            current_player = AvalonGameUser.objects.create(
                game=avalon_game,
                user=user,
                role=role)

        for index in range(len(users)):
            prev, curr, nnext = (index - 1) % len(users), index, (index + 1) % len(users)
            prev = AvalonGameUser.objects.get(game=avalon_game, user=users[prev])
            curr = AvalonGameUser.objects.get(game=avalon_game, user=users[curr])
            nnext = AvalonGameUser.objects.get(game=avalon_game, user=users[nnext])

            prev.next_player = curr
            curr.prev_player = prev
            curr.next_player = nnext
            nnext.prev_player = curr

            prev.save()
            curr.save()
            nnext.save()

        return avalon_game

class AvalonQuest(models.Model):
    game = models.ForeignKey(AvalonGame, related_name='game')

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

    prev_player = models.ForeignKey('AvalonGameUser', related_name='prev', blank=True, null=True)
    next_player = models.ForeignKey('AvalonGameUser', related_name='next', blank=True, null=True)

    role = models.CharField(
        max_length=3,
        choices=GAME_ROLES,
        default=LOYAL_SERVANT)

    def __repr__(self):
        return '<AvalonGameUser game: {g}, user: {u}>'.format(g=self.game.pk, u=self.user.username)