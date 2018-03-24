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
        self.myBase = self.character_state['base']

        # print('junk', self.junks)
        # print('spike', self.spikes)
        # print('grassList', self.grassList)

    def turn(self, game_state, character_state, other_bots):
        super().turn(game_state, character_state, other_bots)

        self.cptTurn += 1
        if self.cptTurn == 1:
            self.firstTurn(game_state, character_state, other_bots)

        self.junks = self.pathfinder.junks
        goalJunk = self.junks[0]
        myLocation = self.character_state['location']
        lengthJunk = self.pathfinder.astar_path_length(myLocation, goalJunk)
        lengthBase = self.pathfinder.astar_path_length(myLocation, self.myBase)
        # print('junk at', lengthJunk)
        # print('base at', lengthBase)
        for bot in self.other_bots:
            botLocation = bot['location']
            lengthBase = self.pathfinder.astar_path_length(botLocation, self.myBase)
            lengthBase = self.pathfinder.astar_path_length(botLocation, myLocation)
            # print('bot', bot['name'], 'at', lengthBase, 'from my base')
            # print('bot', bot['name'], 'at', lengthBase, 'from me')

        direction = self.pathfinder.get_next_direction(myLocation, goalJunk)
        carrying = self.character_state['carrying']
        print('carry', carrying)
        # print(direction)

        self.wasCarrying = carrying

        if direction == None and myLocation == goalJunk and carrying == 0:
            print('grabing')
            return self.commands.collect()
        elif (carrying > 0):
            direction = None
            direction = self.pathfinder.get_next_direction(myLocation, self.myBase)
            print('going back to the base')
            #print('grab', carrying - self.wasCarrying)
            if direction == None and myLocation == self.myBase:
                print('try storing?')
                print(myLocation)
                print(self.myBase)
                return self.commands.store()

        if direction:
            print('is moving!')
            return self.commands.move(direction)
        else:
            return self.commands.idle()


