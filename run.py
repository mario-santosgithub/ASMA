import os
import pandas as pd
import numpy as np

from src.game import tournament
import config as conf

def main():

    if len(conf.params["agents"]) != 4:
        print("Plese select 4 algorithms to compare on the config file.") 
        return
    
    print(conf.params["agents"])
    run = tournament(
        iterations = conf.params['iterations'],
        agents     = conf.params['agents'],
        comment    = conf.params['logging']
    )

    result = pd.concat([
        pd.Series(run[0], name='winner'), 
        pd.Series(run[1], name='turns'),
    ], axis = 1)
    
    # Calculate win rates for each player
    result["win_rate_player_1"] = np.where(result["winner"] == conf.player_name_1, 1, 0)
    result["win_rate_player_1"] = result["win_rate_player_1"].cumsum() / (result.index + 1)

    result["win_rate_player_2"] = np.where(result["winner"] == conf.player_name_2, 1, 0)
    result["win_rate_player_2"] = result["win_rate_player_2"].cumsum() / (result.index + 1)
    
    result["win_rate_player_3"] = np.where(result["winner"] == conf.player_name_3, 1, 0)
    result["win_rate_player_3"] = result["win_rate_player_3"].cumsum() / (result.index + 1)

    result["win_rate_player_4"] = np.where(result["winner"] == conf.player_name_4, 1, 0)
    result["win_rate_player_4"] = result["win_rate_player_4"].cumsum() / (result.index + 1)

    print("winrate player 1: ", result["win_rate_player_1"].iloc[-1])
    print("winrate player 2: ", result["win_rate_player_2"].iloc[-1])
    print("winrate player 3: ", result["win_rate_player_3"].iloc[-1])
    print("winrate player 4: ", result["win_rate_player_4"].iloc[-1])

    q_vals = pd.DataFrame(run[2].q)
    q_vals.index.rename("id", inplace=True)

    # Add columns for the total number of cards played by each player
    result["cards_played_player_1"] = run[3][0]
    result["cards_played_player_2"] = run[3][1]
    result["cards_played_player_3"] = run[3][2]
    result["cards_played_player_4"] = run[3][3]

    # Add columns for hand values
    result["hand_value_player_1"] = run[4][0]
    result["hand_value_player_2"] = run[4][1]
    result["hand_value_player_3"] = run[4][2]
    result["hand_value_player_4"] = run[4][3]

    result["score_player_1"] = run[5][0]
    result["score_player_2"] = run[5][1]
    result["score_player_3"] = run[5][2]
    result["score_player_4"] = run[5][3]

    if not os.path.exists("assets"):
        os.makedirs("assets")

    q_vals.to_csv("assets/q-values.csv", index=True)
    result.to_csv("assets/results.csv", index=False) 
    

if __name__ == "__main__":
    main()