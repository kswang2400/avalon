from game import avalon
from game.tests import setup


class AvalonGameTestCase(setup.AvalonTestCase):
    def setUp(self):
        super(AvalonGameTestCase, self).setUp()

    def test_create_new_game_from_users(self):
        assert self.game

    def test_retrieve_saved_game_with_pk(self):
        game = avalon.Game(pk=self.game.game.pk)
        assert game