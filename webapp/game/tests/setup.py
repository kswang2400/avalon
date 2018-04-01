from django.test import TestCase

from game import avalon
from game.models import AvalonUser


class AvalonTestCase(TestCase):
    def setUp(self):
        self.choi = AvalonUser.objects.create(username="choi", password="foobar")
        self.evan = AvalonUser.objects.create(username="evan", password="foobar")
        self.greg = AvalonUser.objects.create(username="greg", password="foobar")
        self.kent = AvalonUser.objects.create(username="kent", password="foobar")
        self.kevin = AvalonUser.objects.create(username="kevin", password="foobar")
        self.marcus = AvalonUser.objects.create(username="marcus", password="foobar")

        self.game = avalon.Game(users=[
            self.choi,
            self.evan,
            self.greg,
            self.kent,
            self.kevin,
            self.marcus,
        ])