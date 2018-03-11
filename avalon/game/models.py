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
    quest_master = models.ForeignKey(AvalonUser, related_name='quest_master', blank=True, null=True)
    current_quest = models.CharField(
        max_length=1,
        choices=QUEST_CHOICES,
        default='1')

    assasin = models.ForeignKey(AvalonUser, related_name='assasin', blank=True, null=True)
    merlin = models.ForeignKey(AvalonUser, related_name='merlin', blank=True, null=True)
    mordred = models.ForeignKey(AvalonUser, related_name='mordred', blank=True, null=True)
    morgana = models.ForeignKey(AvalonUser, related_name='morgana', blank=True, null=True)
    percival = models.ForeignKey(AvalonUser, related_name='percival', blank=True, null=True)

    loyal_1 = models.ForeignKey(AvalonUser, related_name='loyal_1', blank=True, null=True)
    loyal_2 = models.ForeignKey(AvalonUser, related_name='loyal_2', blank=True, null=True)
    loyal_3 = models.ForeignKey(AvalonUser, related_name='loyal_3', blank=True, null=True)
    loyal_4 = models.ForeignKey(AvalonUser, related_name='loyal_4', blank=True, null=True)

    minion_1 = models.ForeignKey(AvalonUser, related_name='minion_1', blank=True, null=True)
    minion_2 = models.ForeignKey(AvalonUser, related_name='minion_2', blank=True, null=True)
    minion_3 = models.ForeignKey(AvalonUser, related_name='minion_3', blank=True, null=True)
    minion_4 = models.ForeignKey(AvalonUser, related_name='minion_4', blank=True, null=True)

    def __repr__(self):
        return '<AvalonGame users: {u}>'.format(u=self.users)

    @property
    def users(self):
        user_ids = AvalonGameUser.objects.filter(game=self).values_list('id', flat=True)
        return AvalonUser.objects.filter(pk__in=user_ids)

    def create(cls, new_game):
        avalon_game = cls(
            user=new_game.user,
            current_quest=new_game.current_quest)
        avalon_game.save()

        print('\n\navalonguser new game users\n\n')
        print(new_game.users)
        print(len(new_game.users))
        print('\n\n')

        for user in new_game.users:
            current_player = AvalonGameUser.objects.create(
                game=avalon_game,
                user=user)

        for index in range(len(new_game.users)):
            prev, curr, nnext = (index - 1) % len(new_game.users), index, (index + 1) % len(new_game.users)
            print('\n\n{p}\n{c}\n{n}\n\n'.format(p=prev, c=curr, n=nnext))
            prev, curr, nnext = new_game.users[prev], new_game.users[curr], new_game.users[nnext]

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
    user = models.ForeignKey(AvalonUser)
    game = models.ForeignKey(AvalonGame)

    prev_player = models.ForeignKey('AvalonGameUser', related_name='prev', blank=True, null=True)
    next_player = models.ForeignKey('AvalonGameUser', related_name='next', blank=True, null=True)
