import pandas as pd
import numpy as np
import random

import src.state_action_reward as sar


class Agent(object):
    def __init__(self):
        """Initializes the agent to get parameters and create an empty q-tables."""

        self.epsilon     = 0.4
        self.step_size   = 0.2
        self.states      = sar.states()
        self.actions     = sar.actions()
        self.R           = sar.rewards(self.states, self.actions)        

        self.q = pd.DataFrame(
            data    = np.zeros((len(self.states), len(self.actions))), 
            columns = self.actions, 
            index   = self.states
        )
        
        self.visit = self.q.copy()

class LeastValueAgent(Agent):
        
        def __init__(self):
            super().__init__()
        
        def step(self, state_dict, actions_dict, hand):
            """
            Choose the action with the highest Q-value.
            Required parameters:
                - state_dict as dict
                - actions_dict as dict
            """


            minValue = 100
            minIndex = 100
            for card in hand:
                print("min:", minValue)
                print("card:", card.value)
                if type(card.value) != str and card.value != 0 and card.value < minValue:
                    minValue = card.value
                    minIndex = hand.index(card)
            #print("min:", minValue)
            return hand[minIndex].color
        

        def update(self, state_dict, action):
            """
            No update for most value agent.
            Required parameters:
                - state_dict as dict
                - action as str
            """
            pass


class MostValueAgent(Agent):
        
        def __init__(self):
            super().__init__()
        
        def step(self, state_dict, actions_dict, hand):
            """
            Choose the action with the highest Q-value.
            Required parameters:
                - state_dict as dict
                - actions_dict as dict
            """
            actions_possible = [key for key,val in actions_dict.items() if val != 0]

            maxValue = 0
            maxIndex = 0
            print("actionsPossible", actions_possible)
            for card in hand:
                print("numero", card)
                print("max:", maxValue)
                print("card.value:", card.value)
                print("type", type(card.value))
                if type(card.value) != str and card.value != 0 and card.value > maxValue and (card.color in actions_possible):
                    print("é possivel")
                    maxValue = card.value
                    maxIndex = hand.index(card)
                    print("index:", hand.index(card))
                elif card.value in ["SKI", "REV", "PL2"] and card.value in actions_possible:
                    if 20 > maxValue:
                        maxValue = 20
                        maxIndex = hand.index(card)
                    print("index:", hand.index(card))
                elif card.value in ["COL", "PL4"]:
                    if 50 > maxValue:
                        maxValue = 50
                        maxIndex = hand.index(card)
                    print("index:", hand.index(card))
            print("indexMaxFinal:", maxIndex)
            print("indexFinal:", hand[maxIndex].color)
            return maxIndex
        

        def update(self, state_dict, action):
            """
            No update for most value agent.
            Required parameters:
                - state_dict as dict
                - action as str
            """
            pass


class CardCounterAgent(Agent):

    def __init__(self):
        super().__init__()
        self.checker = []
        self.drawn = 0

        # for now just colors
        # 0 = red, 1 = blue, 2 = green, 3 = yellow, 4 = wild
        self.probMatrix = [0,0,0,0,0]

    def step(self, state_dict, actions_dict, hand):
        
        actions_possible = [key for key,val in actions_dict.items() if val != 0]
        minValue = 1000
        minIndex = 0
        for card in actions_possible:
            if card == "RED" and self.probMatrix[0] > minValue:
                minValue = self.probMatrix[0]
                minIndex = actions_possible.index(card)
            elif card == "GRE" and self.probMatrix[1] > minValue:
                minValue = self.probMatrix[1]
                minIndex = actions_possible.index(card)
            elif card == "BLU" and self.probMatrix[2] > minValue:
                minValue = self.probMatrix[2]
                minIndex = actions_possible.index(card)
            elif card == "YEL" and self.probMatrix[3] > minValue:
                minValue = self.probMatrix[3]
                minIndex = actions_possible.index(card)
            elif card == "WILD" and self.probMatrix[4] > minValue:
                minValue = self.probMatrix[4]
                minIndex = actions_possible.index(card)
        return actions_possible[minIndex]


class RandomAgent(Agent):
        
    def __init__(self):
        super().__init__()
    
    def step(self, state_dict, actions_dict, hand):
        """
        Choose a random action.
        Required parameters:
            - state_dict as dict
            - actions_dict as dict
        """

        actions_possible = [key for key,val in actions_dict.items() if val != 0]
        action = random.choice(actions_possible)
        
        return action
    
    def update(self, state_dict, action):
        """
        No update for random agent.
        Required parameters:
            - state_dict as dict
            - action as str
        """
        pass


class QLearningAgent(Agent):
    
    def __init__(self):        
        
        super().__init__()
        self.prev_state  = 0
        self.prev_action = 0
    
    def step(self, state_dict, actions_dict, hand):
        """
        Choose the optimal next action according to the followed policy.
        Required parameters:
            - state_dict as dict
            - actions_dict as dict
        """
        
        # (1) Transform state dictionary into tuple
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (2) Choose action using epsilon greedy
        # (2a) Random action
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]         
            action = random.choice(actions_possible)
        
        # (2b) Greedy action
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],i][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        return action
    
    def update(self, state_dict, action):
        """
        Updating Q-values according to Belman equation
        Required parameters:
            - state_dict as dict
            - action as str
        """
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (1) Set prev_state unless first turn
        if self.prev_state != 0:
            prev_q = self.q.loc[[self.prev_state], self.prev_action][0]
            this_q = self.q.loc[[state], action][0]
            reward = self.R.loc[[state], action][0]
            
            #print ("\n")
            #print (f'prev_q: {prev_q}')
            #print (f'this_q: {this_q}')
            #print (f'prev_state: {self.prev_state}')
            #print (f'this_state: {state}')
            #print (f'prev_action: {self.prev_action}')
            #print (f'this_action: {action}')
            #print (f'reward: {reward}')
            
            # Calculate new Q-values
            if reward == 0:
                self.q.loc[[self.prev_state], self.prev_action] = prev_q + self.step_size * (reward + this_q - prev_q) 
            else:
                self.q.loc[[self.prev_state], self.prev_action] = prev_q + self.step_size * (reward - prev_q)
                
            self.visit.loc[[self.prev_state], self.prev_action] += 1
            
        # (2) Save and return action/state
        self.prev_state  = state
        self.prev_action = action
      
        
class MonteCarloAgent(Agent):

    def __init__(self):

        super().__init__()
        self.state_seen  = list()
        self.action_seen = list()
        self.q_seen      = list()
    
    def step(self, state_dict, actions_dict, hand):
        """
        Choose the optimal next action according to the followed policy.
        Required parameters:
            - state_dict as dict
            - actions_dict as dict
        """
        
        # (1) Transform state dictionary into tuple
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        # (2) Choose action using epsilon greedy
        # (2a) Random action
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]         
            action = random.choice(actions_possible)
        
        # (2b) Greedy action
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],i][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        # (3) Add state-action pair if not seen in this simulation
        if ((state),action) not in self.q_seen:
            self.state_seen.append(state)
            self.action_seen.append(action)
        
        self.q_seen.append(((state),action))
        self.visit.loc[[state], action] += 1
        
        return action
    
    def update(self, state_dict, action):
        """
        Updating Q-values according to Belman equation
        Required parameters:
            - state_dict as dict
            - action as str
        """

        state  = [i for i in state_dict.values()]
        state  = tuple(state)
        reward = self.R.loc[[state], action][0]
        
        # Update Q-values of all state-action pairs visited in the simulation
        for s,a in zip(self.state_seen, self.action_seen): 
            self.q.loc[[s], a] += self.step_size * (reward - self.q.loc[[s], a])
        
        self.state_seen, self.action_seen, self.q_seen = list(), list(), list()
