# Autonomous Agents and Multi-Agent System

### Group 9: 
Vadym Volkovinskyy 86524  
Daniel Gomes 99195  
Mário Santos 99275


## Description
In this project we aim to find some sort of strategy to play the game UNO optimally, for that we use various agents that will play a tournament, where different metrics are taken in consideration.

The agents are: a Random, CardCounter, MostValue, LeastValue, RLOne, RLTwo.

The game is made form a 4 player game at the same time, they can be selected at the config.py file.

## Project Structure

 - `assets/` .csv files with information for the graphics
 - `analysis` a jupyter notebook with the information of winrates and total points of the tournament
 - `src/` core package to simulate games
 - `config.py` configurable parameters
 - `run.py` executation file

## Execution Instruction

Install the necessary packages:

```bash
% pip install -r requirements.txt
```

Execute the run file:

```bash
$ python3 -W ignore run.py
```

Then you can check the results in the jupyter notebook.
