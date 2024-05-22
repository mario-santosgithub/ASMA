import time
import sys

from src.agents import *
from src.players import Player
from src.turn import Turn
from src.cards import Card, Deck
from src.utils import check_win, block_print, enable_print, bold
import config as conf



class Game(object):
    
    def __init__(self, player_1_name, player_2_name, player_3_name, player_4_name, starting_name, agents, comment):
        
        self.player_1 = Player(player_1_name, agent=agents[0])
        self.player_2 = Player(player_2_name, agent=agents[1])
        self.player_3 = Player(player_3_name, agent=agents[2])
        self.player_4 = Player(player_4_name, agent=agents[3])

        rl1Agent = None
        rl1Player = None
        rl2Agent = None
        rl2Player = None
        # Check if there are any RL agents in the game
        for agent in agents:
            if isinstance(agent, RLOneAgent):
                if rl1Agent == None:
                    rl1Agent = agent
            elif isinstance(agent, RLTwoAgent):
                if rl2Agent == None:
                    rl2Agent = agent

        if comment == False: block_print()
        self.turn = Turn(
            deck=Deck(), 
            player_1=self.player_1, 
            player_2=self.player_2,
            player_3=self.player_3, 
            player_4=self.player_4
        )

        self.player = [self.player_1, self.player_2, self.player_3, self.player_4]

        # True - Clockwise, False - Counter-clockwise
        self.flag = True

        self.turn_no = 0
        self.winner = 0

        # Number of cards played by each player
        self.cards_played_player_1 = 0
        self.cards_played_player_2 = 0
        self.cards_played_player_3 = 0
        self.cards_played_player_4 = 0

        # Initialize variables to store the hand values
        self.hand_value_player_1 = 0
        self.hand_value_player_2 = 0
        self.hand_value_player_3 = 0
        self.hand_value_player_4 = 0

        playing_agent = None
        passing_agent = None
        
        # Determine the starting player
        i = 0

        if starting_name == self.player_1.name:
            player_act = self.player_1
            playing_agent = agents[0]
            i = 0

            if self.flag:
                player_pas = self.player_2
                passing_agent = agents[1]
            else:
                player_pas = self.player_4
                passing_agent = agents[3]

        elif starting_name == self.player_2.name:
            player_act = self.player_2
            playing_agent = agents[1]
            i = 1

            if self.flag:
                player_pas = self.player_3
                passing_agent = agents[2]
            else: 
                player_pas = self.player_1
                passing_agent = agents[0]
            
        elif starting_name == self.player_3.name:
            player_act = self.player_3
            playing_agent = agents[2]
            i = 2

            if self.flag:
                player_pas = self.player_4
                passing_agent = agents[3]
            else:
                player_pas = self.player_2
                passing_agent = agents[1]

        else:
            player_act = self.player_4
            playing_agent = agents[3]
            i = 3

            if self.flag:
                player_pas = self.player_1
                passing_agent = agents[0]
            else:
                player_pas = self.player_3
                passing_agent = agents[2]
        

        # With each new game the starting player is switched, in order to make it fair
        while self.winner == 0:
            self.turn_no += 1
            card_open = self.turn.card_open
            bold (f'\n---------- TURN {self.turn_no} ----------')
            print (f'\nCurrent open card: {self.turn.card_open.print_card()}')

            
            player_act.show_hand()
            player_act.show_hand_play(card_open)
            self.turn.action(
                player=player_act, 
                opponent=player_pas, 
                agent=playing_agent
            )

            # Update number of cards played by the active player
            if player_act == self.player_1:
                self.cards_played_player_1 += 1
                
            elif player_act == self.player_2:
                self.cards_played_player_2 += 1

            elif player_act == self.player_3:
                self.cards_played_player_3 += 1

            else:
                self.cards_played_player_4 += 1
            
            if check_win(player_act) == True:
                self.winner = player_act.name
                print (f'{player_act.name} has won!')
                if isinstance(player_act.agent, CardCounterAgent):
                    player_act.agent.probMatrix = [0,0,0,0,0]
                break
                
            if check_win(player_pas) == True:
                self.winner = player_pas.name
                print (f'{player_pas.name} has won!')
                if isinstance(player_pas.agent, CardCounterAgent):
                    player_pas.agent.probMatrix = [0,0,0,0,0]
                break
                
            if player_act.card_play.value == "REV":
                self.flag = not self.flag
                if self.flag:
                    i = (i+1)%4
                else:
                    i = (i-1)%4
        
            elif player_act.card_play.value == "SKI":
                if self.flag:
                    i = (i+2)%4
                else:
                    i = (i-2)%4

            else:
                if self.flag:
                    i = (i+1)%4
                else:
                    i = (i-1)%4

            player_act = self.player[i]
            playing_agent = agents[i]
            if self.flag:
                player_pas = self.player[(i+1)%4]
                passing_agent = agents[(i+1)%4]
            else:
                player_pas = self.player[(i-1)%4]
                passing_agent = agents[(i-1)%4]

        # Update the state-action pairs for the RL agents, if they exist
        if rl1Agent != None:
            self.player_3.identify_state(card_open)
            rl1Agent.update(self.player_3.state, self.player_3.action)

        if rl2Agent != None:
            self.player_4.identify_state(card_open)
            rl2Agent.update(self.player_4.state, self.player_4.action)
                
        if comment == False: enable_print()

        self.hand_value_player_1 = self.player_1.calculate_hand_value()
        self.hand_value_player_2 = self.player_2.calculate_hand_value()
        self.hand_value_player_3 = self.player_3.calculate_hand_value()
        self.hand_value_player_4 = self.player_4.calculate_hand_value()


def selectAgent(behaviour):

    if behaviour == "Random":
        return RandomAgent()
    
    if behaviour == "RLOne":
        return RLOneAgent()
    
    if behaviour == "RLTwo":
        return RLTwoAgent()
    
    if behaviour == "CardCounter":
        return CardCounterAgent()
    
    if behaviour == "MostValue":
        return MostValueAgent()
    
    if behaviour == "LeastValue":
        return LeastValueAgent()

def tournament(iterations, agents, comment):

    timer_start = time.time()
    
    global agentList, agent1, agent2, agent3, agent4

    agentList = []
    agent1 = selectAgent(agents[0])
    agentList.append(agent1)

    agent2 = selectAgent(agents[1])
    agentList.append(agent2)

    agent3 = selectAgent(agents[2])
    agentList.append(agent3)

    agent4 = selectAgent(agents[3])
    agentList.append(agent4)
    
    winners, turns, coverage = list(), list(), list()

    cards_played_player_1_list = list()   # Lists to store cards played by each player
    cards_played_player_2_list = list()  
    cards_played_player_3_list = list()
    cards_played_player_4_list = list()

    hand_value_player_1_list = list() # Lists to store value of hand by each player
    hand_value_player_2_list = list()  
    hand_value_player_3_list = list()
    hand_value_player_4_list = list()


    score_player_1 = 0
    score_player_2 = 0
    score_player_3 = 0
    score_player_4 = 0

    hand_value_player_1_cumsum = list()
    hand_value_player_2_cumsum = list()
    hand_value_player_3_cumsum = list()
    hand_value_player_4_cumsum = list()

    for i in range(iterations):
        time.sleep(0.01)
        #sys.stdout.write(f'\r{i} of {iterations} games completed')1
        sys.stdout.write(f'\r>> {(i/iterations)*100:.1f}% of games completed')
        sys.stdout.flush()
        if i%4 == 1:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                player_3_name=conf.player_name_3,
                player_4_name=conf.player_name_4,
                starting_name=conf.player_name_2,
                agents=agentList,
                comment=comment
            )
        elif i%4 == 2:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                player_3_name=conf.player_name_3,
                player_4_name=conf.player_name_4,
                starting_name=conf.player_name_3,
                agents=agentList,
                comment=comment
            )
        elif i%4 == 3:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                player_3_name=conf.player_name_3,
                player_4_name=conf.player_name_4,
                starting_name=conf.player_name_4,
                agents=agentList,
                comment=comment
            )
        else:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                player_3_name=conf.player_name_3,
                player_4_name=conf.player_name_4,
                starting_name=conf.player_name_1,
                agents=agentList,
                comment=comment
            )

        winners.append(game.winner)
        turns.append(game.turn_no)
        # only if its q-learning, change later
        coverage.append((agent2.q != 0).values.sum())

        cards_played_player_1_list.append(game.cards_played_player_1)
        cards_played_player_2_list.append(game.cards_played_player_2)
        cards_played_player_3_list.append(game.cards_played_player_3)
        cards_played_player_4_list.append(game.cards_played_player_4)

        hand_value_player_1_list.append(game.hand_value_player_1)
        hand_value_player_2_list.append(game.hand_value_player_2)
        hand_value_player_3_list.append(game.hand_value_player_3)
        hand_value_player_4_list.append(game.hand_value_player_4)

        score_player_1 += game.hand_value_player_1
        score_player_2 += game.hand_value_player_2
        score_player_3 += game.hand_value_player_3
        score_player_4 += game.hand_value_player_4

        hand_value_player_1_cumsum.append(score_player_1)
        hand_value_player_2_cumsum.append(score_player_2)
        hand_value_player_3_cumsum.append(score_player_3)
        hand_value_player_4_cumsum.append(score_player_4)

    # Calculate the total points for each player
    total_points_player_1 = hand_value_player_1_cumsum[-1]
    total_points_player_2 = hand_value_player_2_cumsum[-1]
    total_points_player_3 = hand_value_player_3_cumsum[-1]
    total_points_player_4 = hand_value_player_4_cumsum[-1]

    overall_points = 0
    # Determine the winner of the tournament based on total points
    if total_points_player_1 < total_points_player_2 and total_points_player_1 < total_points_player_3 and total_points_player_1 < total_points_player_4:
        overall_winner = conf.player_name_1
        overall_points = total_points_player_1
    elif total_points_player_2 < total_points_player_1 and total_points_player_2 < total_points_player_3 and total_points_player_2 < total_points_player_4:
        overall_winner = conf.player_name_2
        overall_points = total_points_player_2
    elif total_points_player_3 < total_points_player_1 and total_points_player_3 < total_points_player_2 and total_points_player_3 < total_points_player_4:
        overall_winner = conf.player_name_3
        overall_points = total_points_player_3
    elif total_points_player_4 < total_points_player_2 and total_points_player_4 < total_points_player_3 and total_points_player_4 < total_points_player_1:
        overall_winner = conf.player_name_4
        overall_points = total_points_player_4
    else:
        overall_winner = "It's a tie"
        overall_points = 0
        # it its never hapening
        
    # Timer
    timer_end = time.time()
    timer_dur = timer_end - timer_start
    print (f'Execution lasted {round(timer_dur/60,2)} minutes ({round(iterations/timer_dur,2)} games per second)')
    # print(f'The winner of the tournament is: {overall_winner} with {total_points_player_1} points vs {total_points_player_2} points')
    print(f'The winner of the tournament is: {overall_winner} with {overall_points}')
    
    cardPlayedList = [cards_played_player_1_list, cards_played_player_2_list, cards_played_player_3_list, cards_played_player_4_list]
    handValueList = [hand_value_player_1_list, hand_value_player_2_list, hand_value_player_3_list, hand_value_player_4_list]
    finalPointsList = [hand_value_player_1_cumsum, hand_value_player_2_cumsum, hand_value_player_3_cumsum, hand_value_player_4_cumsum]

    return winners, turns, agent2, cardPlayedList, handValueList, finalPointsList