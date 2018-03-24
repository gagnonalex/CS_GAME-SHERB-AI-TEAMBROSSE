from src.bot.Bot2 import Bot
from src.symbols.ObjectSymbols import ObjectSymbols


class PythonBot2(Bot):

    def __init__(self):
        super().__init__()
        # self.cptTurn = 0

    def get_name(self):
        return 'Python2'

    def firstTurn(self, game_state, character_state, other_bots):
        # graph = self.pathfinder.create_graph(self.pathfinder.game_map)
        self.junks = self.pathfinder.junks
        self.spikes = self.pathfinder.spikes
        self.grassList = self.pathfinder.grassList

        print('junk', self.junks)
        print('spike', self.spikes)
        print('grassList', self.grassList)

    def turn(self, game_state, character_state, other_bots):
        super().turn(game_state, character_state, other_bots)

        self.cptTurn += 1
        print(self.cptTurn)
        if self.cptTurn == 1:
            self.firstTurn(game_state, character_state, other_bots)

        self.junks = self.pathfinder.junks
        goalJunk = self.junks[0]
        lengthJunk = self.pathfinder.astar_path_length(self.character_state['location'], goalJunk)
        print('junk at', lengthJunk)
        print(self.character_state)
        length_base = self.pathfinder.astar_path_length(self.character_state['location'], self.character_state['base'])


        goal = (1, 1)

        direction = self.pathfinder.get_next_direction(self.character_state['location'], goal)
        if direction:
            return self.commands.move(direction)
        else:
            return self.commands.idle()

