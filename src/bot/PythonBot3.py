from src.bot.Bot3 import Bot
from src.symbols.ObjectSymbols import ObjectSymbols


class PythonBot3(Bot):

    def __init__(self):
        super().__init__()
        # self.cptTurn = 0

    def get_name(self):
        return 'Python3'

    def firstTurn(self, game_state):
        # graph = self.pathfinder.create_graph(self.pathfinder.game_map)
        self.pathfinder.parse_game_state_first_turn(game_state)
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
            self.firstTurn(game_state)

        goalJunk = self.junks[self.junkIndex]
        self.myLocation = self.character_state['location']
        lengthJunk = self.pathfinder.astar_path_length(self.myLocation, goalJunk)
        lengthBase = self.pathfinder.astar_path_length(self.myLocation, self.myBase)
        # print('junk at', lengthJunk)
        # print('base at', lengthBase)
        for bot in self.other_bots:
            botLocation = bot['location']
            # lengthBase = self.pathfinder.astar_path_length(botLocation, self.myBase)
            # lengthBase = self.pathfinder.astar_path_length(botLocation, myLocation)
            # print('bot', bot['name'], 'at', lengthBase, 'from my base')
            # print('bot', bot['name'], 'at', lengthBase, 'from me')
            if abs(botLocation[0] - self.myLocation[0]) == 1 and botLocation[1] == self.myLocation[1]:
                print('try attack 0')
                print(botLocation)
                print(self.myLocation)
                if(botLocation[0] - self.myLocation[0]) == 1:
                    return self.commands.attack('S')
                else:
                    return self.commands.attack('N')

            elif abs(botLocation[1] - self.myLocation[1]) == 1 and botLocation[0] == self.myLocation[0]:
                print('try attack 1')
                print(botLocation)
                print(self.myLocation)
                if(botLocation[1] - self.myLocation[1]) == 1:
                    return self.commands.attack('E')
                else:
                    return self.commands.attack('W')

        direction = self.pathfinder.get_next_direction(self.myLocation, goalJunk)
        carrying = self.character_state['carrying']

        # print('longeur des junks')
        # print(self.junks)

        self.wasCarrying = carrying

        if  self.myLocation == goalJunk and self.outOfTenDig <10:
            # print('grabing')
            self.outOfTenDig+=1
            return self.commands.collect()

        # elif (carrying > 0 and self.outOfTenDig <10):
        #

        elif (self.outOfTenDig ==10):
            print('******************* 10 finishm now nxt junk')
            self.visitedJunk.append(self.junks[self.junkIndex])
            if self.junks[self.junkIndex+1] in self.visitedJunk:
                print('DEJA VISITER DUDE')
            self.junkIndex += 1
            self.outOfTenDig = 0
            self.junkIndex +=1

        if direction:
            # print('is moving!')
            return self.commands.move(direction)
        else:
            return self.commands.idle()

def goingBack(self):

    direction = None
    #  direction = self.pathfinder.get_next_direction(myLocation, self.myBase)
    # print('going back to the base')
    #print('grab', carrying - self.wasCarrying)
    if direction == None and self.myLocation == self.myBase:
        # print('try storing?')
        # print(myLocation)
        # print(self.myBase)
        return self.commands.store()