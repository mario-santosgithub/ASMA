# While choosing the agents, plase select the following options:
# "Random" - RandomAgent
# "MostValue" - Agent that plays the card with the highest value
# "LeastValue" - Agent that plays the card with the lowest value
# "CardCounter" - Agent that plays the card with the least amount of cards
# "RLOne" - Agent that uses the Q-learning algorithm (On Position 3)
# "RLTwo" - Agent that uses the Monte Carlo algorithm (On Position 4)

# Note: if using RL agents, use "RLOne" and "RLTwo" as player names, in places 3 and 4 respectively.
# Chose on the Agents and their respective names below

params = {
    "iterations": 200,  # <- Number of games to play in the tournament
    "agents": [
        "Random",
        "CardCounter",
        "MostValue",
        "LeastValue"
    ],
    "logging": False
}


player_name_1 = "Random"
player_name_2 = "CardCounter"
player_name_3 = "RLOne"
player_name_4 = "RLTwo"
