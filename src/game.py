import time
import sys

from src.agents import *
from src.players import Player
from src.turn import Turn
from src.cards import Card, Deck
from src.utils import check_win, block_print, enable_print, bold
import config as conf



class Game(object):
    """ 
    A game reflects an iteration of turns, until one player fulfills the winning condition of 0 hand cards.
    It initialized with two players and a turn object.
    """
    def __init__(self, player_1_name, player_2_name, starting_name, agents, comment):
        
        if comment == False: block_print()
        self.player_1 = Player(player_1_name, agent=agents[0])
        self.player_2 = Player(player_2_name, agent=agents[1])
        self.turn = Turn(
            deck=Deck(), 
            player_1=self.player_1, 
            player_2=self.player_2
        )
        
        self.turn_no = 0
        self.winner = 0

        # With each new game the starting player is switched, in order to make it fair
        while self.winner == 0:
            self.turn_no += 1
            card_open = self.turn.card_open
            bold (f'\n---------- TURN {self.turn_no} ----------')
            print (f'\nCurrent open card: {self.turn.card_open.print_card()}')

            playing_agent = None
            passing_agent = None

            if starting_name == self.player_1.name:
                if self.turn_no%2 == 1: 
                    player_act, player_pas = self.player_1, self.player_2
                    playing_agent, passing_agent = agents[0], agents[1]
                else:                   
                    player_act, player_pas = self.player_2, self.player_1
                    playing_agent, passing_agent = agents[1], agents[0]
            else:
                if self.turn_no%2 == 0: 
                    player_act, player_pas = self.player_1, self.player_2
                    playing_agent, passing_agent = agents[0], agents[1]
                else:                   
                    player_act, player_pas = self.player_2, self.player_1
                    playing_agent, passing_agent = agents[1], agents[0]

            player_act.show_hand()
            player_act.show_hand_play(card_open)
            self.turn.action(
                player=player_act, 
                opponent=player_pas, 
                agent=playing_agent
            )
            
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
                
            if player_act.card_play.value in ["REV", "SKIP"]:
                print (f'{player_act.name} has another turn')
                self.turn_no = self.turn_no-1
                
            if (self.turn.count > 0) and (self.turn.count %2 == 0):
                print (f'Again it is {player_act.name}s turn')
                self.turn_no = self.turn_no-1
        

        self.player_2.identify_state(card_open)
        if isinstance(agents[1], QLearningAgent) or isinstance(agents[1], MonteCarloAgent):
            agents[1].update(self.player_2.state, self.player_2.action)
                
        if comment == False: enable_print()


def selectAgent(behaviour):

    if behaviour == "Random":
        return RandomAgent()
    
    if behaviour == "monte-carlo":
        return MonteCarloAgent()
    
    if behaviour == "CardCounter":
        return CardCounterAgent()
    
    if behaviour == "MostValue":
        return MostValueAgent()
    
    if behaviour == "LeastValue":
        return LeastValueAgent()

def tournament(iterations, agents, comment):
    """
    A function that iterates various Games and outputs summary statistics over all executed simulations.
    """
    timer_start = time.time()
    
    # Selection of algorithm
    global agentList, agent1, agent2

    # POR ENQUANTO APENAS 2 AGENTES
    agentList = []
    agent1 = selectAgent(agents[0])
    agentList.append(agent1)

    agent2 = selectAgent(agents[1])
    agentList.append(agent2)

    #if agents[0] == "q-learning":
    #    agent = QLearningAgent()
    #else:
    #    agent = MonteCarloAgent()
    
    winners, turns, coverage = list(), list(), list()

    for i in range(iterations):
        time.sleep(0.01)
        #sys.stdout.write(f'\r{i} of {iterations} games completed')1
        sys.stdout.write(f'\r>> {(i/iterations)*100:.1f}% of games completed')
        sys.stdout.flush()
        if i%2 == 1:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                starting_name=conf.player_name_2,
                agents=agentList,
                comment=comment
            )
        else:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                starting_name=conf.player_name_1,
                agents=agentList,
                comment=comment
            )

        winners.append(game.winner)
        turns.append(game.turn_no)
        coverage.append((agent2.q != 0).values.sum())

    # Timer
    timer_end = time.time()
    timer_dur = timer_end - timer_start
    print (f'Execution lasted {round(timer_dur/60,2)} minutes ({round(iterations/timer_dur,2)} games per second)')
    
    return winners, turns, agent2