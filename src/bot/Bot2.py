from src.bot.Commands import Commands
from src.command.Idle import Idle
from src.utils.Pathfinder2 import Pathfinder


class Bot:

    def __init__(self):
        self.player_id = None
        self.game_state = None
        self.character_state = None
        self.other_bots = None
        self.commands = None
        self.pathfinder = Pathfinder()
        self.junks = []
        self.spikes = []
        self.grassList = []
        self.cptTurn = 0
        # self.carrying = 0
        self.wasCarrying = 0
        self.myBase = ''
        self.visitedJunk = []
        self.junkIndex = 0
        self.outOfTenDig = 0
        self.outOfTenSum = 0
        self.myLocation = ''
        self.state = 'exploration'
    def set_player_id(self, player_id):
        self.player_id = player_id
        self.commands = Commands(player_id)

    def get_name(self):
        raise NotImplementedError

    def turn(self, game_state, character_state, other_bots):
        self.game_state = game_state
        self.character_state = character_state
        self.other_bots = other_bots
        self.pathfinder.set_game_state(game_state, other_bots)
        return Idle(self.player_id)
