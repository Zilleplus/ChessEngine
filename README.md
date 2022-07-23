# General Architecture
- Uses Python-Chess to keep track of the game state, and read out pgn files.
- Agents are implementations of algorithms to play chess

# Tools
- bot_vs_bot.py: let two bots play against each other.
- human_vs_bot.py: play agains one of the agents, your white, and the agent is black.
- simulate.py: simulate a bunch of games in parallel, summarize the scores, and return the result. (at the moment the multi-processing does not work well with tensorflow, use simulate_serial.py instead)

# RandomAgent
The random agent plays a (uniformly distributed) random move, it's used to benchmark against more complicated agents.

# MinMaxAgent and MinMaxAlphaBetaAgent

## Algorithm
The min-max algorithm is nice described on [wikipedia](https://en.wikipedia.org/wiki/Minimax), to check this out if you not familiar with it.

In a nutshell, it's a tree search algorithm that searches all posibilities. It applies all possible moves for a certain depth, then evaluates the position using a value function. And then returns the move with the best score.
It's very slow, as it tries all posibilites, a minor improvement is the alpha beta pruning: If your opponent has one amazing countermove to a certain move. You can prune the entire branch. 
Both classical min-max and min-max with alpha beta pruning is implemented. A depth of 3 seems to be playable on my pc.

## Value function
The value function takes as input the board state and returns a floating point score that represents how good a situation is for the player that can make a move.

There are implementations of the value function
1. Classical material score: The way chess players count
2. A trained value function: CNN using keras, a learned value function.

# Training of a value function used with the minmax algorithm

## Step 1: Prepare the data

The database used: http://caissabase.co.uk/

Extract the files (Scid file format) into the database folder
You should have 3 files:
1. index file: Caissabase_2022_01_08.si4
2. name file: Caissabase_2022_01_08.sn4
3. game file: Caissabase_2022_01_08.sg4
More info at: http://scidvspc.sourceforge.net/doc/Formats.htm#:~:text=Scid%20Databases%20consist%20of%20three,sg4).

Convert the files to png format so it can read by python-chess.

Launch the generate data script to create the data. The script will:
1. Load a game.
2. Loop through all the moves.
3. Save the state of the entire board at everymove, with the result.

The result is a file called "database_processed.npz", it contains 2 matrices. X and Y. 
- Y: shape=(num_of_samples, 1) -> 1 if white wins, 0 if draw and -1 if black wins.
- X: shape=(num_of_samples, 8, 8, 12) -> the second and third dimension represent the 8*8 grid. The last dimension is the piece type, but one hot encoded. (converted to float32 type)

## Step 2: Train the neural network
Launch the train.py script, if no "trial_network.keras" file from a previous run exists, it will create a new model. Otherwise it will load the model from the keras file. And start training it using the dataset created in step 1. After every epoch the result is saved in trial_network.keras .

- The database is split into two, one validation one training.
- The input layer of the neural network expects a tensor of shape: (BatchSize, 8, 8, 12)
- The batch size is 512, this seems to work great on my nvidea 3060.

## Step 3: let's play agains a random agent.
If out value function has any meaning it should win against a random agent. e.g. One that just plays random moves.

Run the bot_vs_bot.py script, the neural network minmax algorthm plays white. The random agent play's black. The random agent will play a random valid move. A local run on my computer with a neural network with very limited training time gives:

```
r . . . q b n .
p . B . p . p r
. . . . K . P p
. P k . . . . .
. . . . p P . .
. P . . . . . .
P . . . . . . .
. . . . . . . R

white score is 13
black score is 30
```

The score is the "Classical material score" value function. The game ends after 40 moves, as checkmating is very hard without some specialized logic.

There is also simulate.py, which can simulate a bunch of games in parallel, so you get a statistical sense of how good your agent is.