# ChessEngine using Min Max Algorithm

## Value function
Floating point score that represents how good a situation is for the player that can make a move.

There are implementations of the value function
1. Classical material score: The way chess players count
2. A trained value function: CNN using keras, a learned value function.

## Training of the value function

### Step 1: Prepare the data

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

### Step 2: Train the neural network
Launch the train.py script, if no "trial_network.keras" file from a previous run exists, it will create a new model. Otherwise it will load the model from the keras file. And start training it using the dataset created in step 1. After every epoch the result is saved in trial_network.keras .

- The database is split into two, one validation one training.
- The input layer of the neural network expects a tensor of shape: (BatchSize, 8, 8, 12)
- The batch size is 512, this seems to work great on my nvidea 3060.

### Step 3: let's play agains a random agent.
If out value function has any meaning it should win against a random agent. e.g. One that just plays random moves.

Run the bot_vs_bot.py script, the neural network minmax algorthm plays white. The random agent play's black. The random agent will play a random valid move. A local run on my computer with a neural network with very limited training time gives:

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

The score is the "Classical material score" value function. The game ends after 40 moves, as checkmating is very hard without some specialized logic.

There is also simulate.py, which can simulate a bunch of games in parallel, so you get a statistical sense of how good your agent is.
