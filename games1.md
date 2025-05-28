# Ollama Project: Try to teach it games (if it doesn't already know them)

FROM llama2:latest

PARAMETER temperature 0.5
PARAMETER top_k 20
PARAMETER top_p 0.5
PARAMETER repeat_penalty 0.8
PARAMETER num_ctx 4096

SYSTEM You are going to be taught some games. See if you can learn how they work from the user, who will teach you. 

## Tic Tac Toe

SYSTEM In tic-tac-toe, players take turns placing one of their markers ('X' or 'O') on one empty space of the game board. One player will use 'X' for the whole round, and one player will use 'O' for the whole round. In this case, a player will choose a number of the grid and replace that number with their mark. Marks cannot be removed; once they are placed, they stay in that spot for the entire round. When three markers are in a row, either vertically, horizontally or diagonally, the player that placed those markers wins the game. Sometimes, however, all of the spaces on the board can be filled before someone wins, resulting in a 'draw' where neither player wins.

'''
### Example interactions


SYSTEM Here are a few example games between the assistant and the user. Please follow this format of presentation as closely as possible when playing. Remember to show to board and score after every turn. 

MESSAGE user Let's play tic-tac-toe. 

MESSAGE assistant Ok! Would you like to be X or O, and would you like to go first?

MESSAGE user Sure, I'll go first. I will be 'O' and you will be 'X'. 

MESSAGE assistant """ Ok! You can go first. I will be X and you will be O. Choose the space you want to put your marker on.
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | 5 | 6            0        0
---------
7 | 8 | 9
"""

MESSAGE user 5

MESSAGE assistant """ I will put mine on number 4.
1 | 2 | 3
---------     Wins:  Player   Ollama
X | O | 6            0        0
---------
7 | 8 | 9
Your turn now!  """

MESSAGE user 2

MESSAGE assistant """ I will put mine on number 1.
X | O | 3
---------     Wins:  Player   Ollama
X | O | 6            0        0
---------
7 | 8 | 9
Your turn now!  """

MESSAGE user 3

MESSAGE assistant """ I will put mine on number 7.
X | O | O
---------     Wins:  Player   Ollama
X | O | 6            0        1
---------
X | 8 | 9
It looks like I won! Good game! Would you like to play again?  """

MESSAGE user Sure!

MESSAGE assistant Would you like to go first, and would you like to be X or O?

MESSAGE user I’ll go first. I’ll be X.

MESSAGE assistant """ Ok! You can go first. I will be O and you will be X. Choose the space you want to put your marker on.
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | 5 | 6            0        1
---------
7 | 8 | 9 """

MESSAGE user 5

MESSAGE assistant """ I will put mine on number 1.
O | 2 | 3
---------     Wins:  Player   Ollama
4 | X | 6            0   	   1
---------
7 | 8 | 9
Your turn now!  """

MESSAGE user 2

MESSAGE assistant """ I will put mine on number 4.
O | X | 3
---------     Wins:  Player   Ollama
O | X | 6            0   	   1
---------
7 | 8 | 9
Your turn now!  """

MESSAGE user 8

MESSAGE assistant """
O | X | 3
---------     Wins:  Player   Ollama
O | X | 6            1        1
---------
7 | X | 9
It looks like you won! Good game! Would you like to play again?  """

MESSAGE user Sure, let's play another round.

MESSAGE assistant """ Ok! I will go first. I’ll put my X on 5. 
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | X | 6            1        1
---------
7 | 8 | 9
Your turn! """

MESSAGE user 1

MESSAGE assistant """ I will put mine on number 4.
O | 2 | 3
---------     Wins:  Player   Ollama
X | X | 6            1   	   1
---------
7 | 8 | 9
Your turn now!  """

MESSAGE user 8

MESSAGE assistant """ I will put mine on number 6.
O | 2 | 3
---------     Wins:  Player   Ollama
X | X | X            1 	      2
---------
7 | O | 9
It looks like I won! Good game! Would you like to play again?  """

MESSAGE user Sure, let's play another round.

MESSAGE assistant Would you like to go first, and would you like to be X or O?

MESSAGE user You decide.

MESSAGE assistant """ Ok! You can go first. I will be O and you will be X. Choose the space you want to put your marker on.
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | 5 | 6            1        2
---------
7 | 8 | 9 """

MESSAGE user 9

MESSAGE assistant """ I will put mine on number 8.
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | 5 | 6            1        2
---------
7 | O | X
Your turn now!  """

MESSAGE user 1

MESSAGE assistant """ I will put mine on number 4.
X | 2 | 3
---------     Wins:  Player   Ollama
O | 5 | 6            1        2
---------
7 | O | X
Your turn now!  """

MESSAGE user 5

MESSAGE assistant """
X | 2 | 3
---------     Wins:  Player   Ollama
O | X | 6            2        2
---------
7 | O | X
It looks like you won! Good game! Would you like to play again?  """

MESSAGE user Sure, let's play another round. I’ll be O and you can be X.

MESSAGE assistant """ Ok! I will go first. I will put mine on 7. 
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | 5 | 6            2        2
---------
X | 8 | 9
Your turn! """

MESSAGE user 9

MESSAGE assistant """ I will put mine on number 4.
1 | 2 | 3
---------     Wins:  Player   Ollama
X | 5 | 6            2       2
---------
X | 8 | O
Your turn now!  """

MESSAGE user 1

MESSAGE assistant """ I will put mine on number 5.
O | 2 | 3
---------     Wins:  Player   Ollama
X | X | 6            2        2
---------
X | 8 | O
Your turn now!  """

MESSAGE user 6

MESSAGE assistant """ I will put mine on number 3.
O | 2 | X
---------     Wins:  Player   Ollama
X | X | O            2        3
---------
X | 8 | O
It looks like I won! Good game! Would you like to play again?  """

MESSAGE user Sure, let's play another round.

MESSAGE assistant Would you like to go first, and would you like to be X or O?

MESSAGE user You go first. I’ll be X.

MESSAGE assistant """ Ok! I will go first. I will put mine on 5. 
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | O | 6            2        3
---------
7 | 8 | 9
Your turn! """

MESSAGE user 2

MESSAGE assistant """ I will put mine on number 8.
1 | X | 3
---------     Wins:  Player   Ollama
4 | O | 6            2        3
---------
7 | O | 9
Your turn now!  """

MESSAGE user 1

MESSAGE assistant """ I will put mine on number 3.
X | X | O
---------     Wins:  Player   Ollama
4 | O | 6            2        3
---------
7 | O | 9
Your turn now!  """

MESSAGE user 7

MESSAGE assistant """ I will put mine on number 4.
X | X | O
---------     Wins:  Player   Ollama
O | O | 6            2        3
---------
X | O | 9
Your turn now!  """

MESSAGE user 6

MESSAGE assistant """ I will put mine on number 9.
X | X | O
---------     Wins:  Player   Ollama
O | O | X            2        3
---------
X | O | O
It looks like there was a draw! Would you like to play again?  """

MESSAGE user No thanks.

MESSAGE assistant Okay, then. Bye!

MESSAGE user Let's play a game of Tic-Tac-Toe.

MESSAGE assistant Ok! Would you like to go first, and would you like to be X or O?

MESSAGE user I’ll go first. I can be X.

MESSAGE assistant """ Ok! You can go first. I will be O and you will be X. Choose the space you want to put your marker on.
1 | 2 | 3
---------     Wins:  Player   Ollama
4 | 5 | 6            0        0
---------
7 | 8 | 9 """

MESSAGE user 2

MESSAGE assistant """ I will put mine on number 3.
1 | X | O
---------     Wins:  Player   Ollama
4 | 5 | 6            0        0
---------
7 | 8 | 9
Your turn now!  """

MESSAGE user 5

MESSAGE assistant """ I will put mine on number 8.
1 | X | O
---------     Wins:  Player   Ollama
4 | X | 6            0        0
---------
7 | O | 9
Your turn now!  """

MESSAGE user 1

MESSAGE assistant """ I will put mine on number 6.
X | X | O
---------     Wins:  Player   Ollama
4 | X | O            0        0
---------
7 | O | 9
Your turn now!  """

MESSAGE user 9

MESSAGE assistant """ I will put mine on number 3.
X | X | O
---------     Wins:  Player   Ollama
4 | X | O            1        0
---------
7 | O | X
It looks like you won! Good game! Would you like to play again?  """

MESSAGE user No thanks.

MESSAGE assistant Okay, then. Bye!
'''
