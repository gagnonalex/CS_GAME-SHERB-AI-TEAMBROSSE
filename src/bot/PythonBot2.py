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
        self.pathfinder.parse_game_state_first_turn(game_state)
        self.junks = self.pathfinder.junks
        self.spikes = self.pathfinder.spikes
        self.grassList = self.pathfinder.grassList
        self.myBase = self.character_state['base']
        self.openJunks = self.junks



        # print('junk', self.junks)
        # print('spike', self.spikes)
        # print('grassList', self.grassList)

    def turn(self, game_state, character_state, other_bots):
        super().turn(game_state, character_state, other_bots)
        self.harvestTimes = max(1,self.harvestTimes-character_state['respawn'])
        print('carac state')
        print(character_state)
        self.cptTurn += 1
        if self.cptTurn == 1:
            self.firstTurn(game_state, character_state, other_bots)


        self.junks = self.pathfinder.junks
        # goalJunk = self.junks[self.junkIndex]

        self.myLocation = self.character_state['location']

        for bot in self.other_bots:
            botLocation = bot['location']
            # print(botLocation)
            # print(botLocation[0])
            # print(botLocation[1])
            lengthBase = self.pathfinder.astar_path_length(botLocation, self.myBase)
            lengthBase = self.pathfinder.astar_path_length(botLocation, self.myLocation)
            # print('bot', bot['name'], 'at', lengthBase, 'from my base')
            # print('bot', bot['name'], 'at', lengthBase, 'from me')
            if abs(botLocation[0] - self.myLocation[0]) == 1 and botLocation[1] == self.myLocation[1]:
                if(botLocation[0] - self.myLocation[0]) == 1:
                    return self.commands.attack('S')
                else:
                    return self.commands.attack('N')

            elif abs(botLocation[1] - self.myLocation[1]) == 1 and botLocation[0] == self.myLocation[0]:

                if(botLocation[1] - self.myLocation[1]) == 1:
                    return self.commands.attack('E')
                else:
                    return self.commands.attack('W')
        print('state')
        print(self.state)
        # direction = self.pathfinder.get_next_direction(self.myLocation, goalJunk)
        carrying = self.character_state['carrying']

        wasCarrying = self.wasCarrying
        self.wasCarrying = carrying

        if self.state == 'b2b' :
            if(self.myLocation == self.myBase and carrying>0) :
                return self.commands.store()

            elif(self.myLocation == self.myBase and carrying==0 and character_state['health']<100) :
                return self.commands.rest()

            elif(self.myLocation == self.myBase and carrying==0 and character_state['health']==100) :
                self.state = 'harvest'


            direction = self.pathfinder.get_next_direction(self.myLocation, self.myBase)

        elif self.state == 'harvest' :

            if self.firstHarvest :
                maximum = 0

                for postVisited,meanVisited in self.visitedJunk :
                    rep = meanVisited/self.pathfinder.astar_path_length(botLocation, self.myBase)
                    if rep>maximum :
                        maximum = rep
                        self.goal = postVisited
                        self.goalgoalLen = self.pathfinder.astar_path_length(botLocation, self.myBase)


                self.firstHarvest = False
            else :
                if self.myLocation == self.goal :
                    harvestCpt += 1
                    if self.harvestCpt < self.harvestTimes*self.goalLen :

                    else :

                        return self.commands.collect()


            direction = self.pathfinder.get_next_direction(self.myLocation, self.goal)


        elif self.state == 'exploration' :
            minimum = self.pathfinder.astar_path_length(self.myLocation, self.openJunks[0])+1
            coord = ''
            print('openjunk')
            print(self.openJunks)
            for junk in self.openJunks :
                junk_len = self.pathfinder.astar_path_length(self.myLocation, junk)
                if junk_len < minimum :
                    minimum = junk_len
                    goalJunk = junk

            direction = self.pathfinder.get_next_direction(self.myLocation, goalJunk)

            if self.myLocation == goalJunk and self.outOfTenDig <10:
                # print('grabing')
                self.outOfTenSum +=  - self.wasCarrying
                self.outOfTenDig+=1
                return self.commands.collect()

            # elif (carrying > 0 and self.outOfTenDig <10):
            #
            #     direction = None
            #     #  direction = self.pathfinder.get_next_direction(myLocation, self.myBase)
            #     # print('going back to the base')
            #     #print('grab', carrying - self.wasCarrying)
            #     if direction == None and myLocation == self.myBase:
            #         # print('try storing?')
            #         # print(myLocation)
            #         # print(self.myBase)
            #         return self.commands.store()
            elif (self.outOfTenDig ==10):
                self.outOfTenSum = carrying - wasCarrying

                self.visitedJunk.append((goalJunk,self.outOfTenSum))
                self.openJunks.remove(goalJunk)
                print('op junks une delete')
                print(self.openJunks)
                if len(self.openJunks) == 0 :
                    self.state = 'b2b'

                else :
                    self.junkIndex += 1
                    self.outOfTenDig = 0
                    self.junkIndex +=1

        if character_state['spawn'] ==1 :
            harvestTimes -=1
        if direction:
            print('is moving!')
            return self.commands.move(direction)
        else:
            return self.commands.idle()
