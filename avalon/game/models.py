from django.db import models
from django.contrib.auth.models import AbstractUser


class AvalonUser(AbstractUser):
    def __repr__(self):
        return self.username

class AvalonGame(models.Model):
    user = models.ForeignKey(AvalonUser)

    @property
    def users(self):
        user_ids = AvalonGameUser.objects.filter(game=self).values_list('id', flat=True)
        return AvalonUser.objects.filter(pk__in=user_ids)

    @classmethod
    def create(cls, game):
        print('\n\nsave game data\n\n')
        avalon_game = cls(**game.get_table_configs())
        avalon_game.save()

        return avalon_game

class AvalonQuest(models.Model):
    game = models.ForeignKey(AvalonGame, related_name='quests')

class AvalonGameUser(models.Model):
    user = models.ForeignKey(AvalonUser)
    game = models.ForeignKey(AvalonGame)
