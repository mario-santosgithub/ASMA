params = {
    "iterations": 200,
    "agents": [
        "Random",
        "monte-carlo",
        "MostValue",
        "CardCounter",
    ], # ["q-learning", "monte-carlo"]
    "logging": False,
    "model": {
        "epsilon": 0.4,
        "step_size": 0.2,
    }
}

# Please, make the names 1 to for, the same order as the agents above. Thanks!
# Possible agents:
"Random, MostValue, LeastValue, CardCounter, monte-carlo, q-learning"

player_name_1 = "Random"
player_name_2 = "monte-carlo"
player_name_3 = "MostValue"
player_name_4 = "CardCounter"
