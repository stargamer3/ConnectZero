# ConnectZero
Connect 6 bot, should be trainable on other games
## USAGE
Right now running connect6NNMCTS.py should train a model, and there isn't a file here yet to run the model. NNMCTS.py is a general neural network MCTS, with no rollouts, similar to AlphaZero. SimpleMCTS.py is an implementation of standard MCTS for general games, connect6MCTS is a usage example. connect4.py can be used to play connect 4 with a simple MCTS. Connect6.h5 is an untrained connect 6 model. When running connect6NNMCTS.py, after every game it will print: Player1 loss, Player2 loss, game outcome, number of games played so far, amount of time the game took.
