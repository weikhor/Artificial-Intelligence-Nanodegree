"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    len_player = len(game.get_legal_moves(player))
    len_opponent = len(game.get_legal_moves(game.get_opponent(player)))
    # put float make number decimal from github answer
    return float(len_player/8) - float(len_opponent/8)
    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    len_player = len(game.get_legal_moves(player))
    len_opponent = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(len_player/8) - 2*float(len_opponent/8)
    

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    len_player = len(game.get_legal_moves(player))
    len_opponent = len(game.get_legal_moves(game.get_opponent(player)))
    
    return len_player - 2*len_opponent
    

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            #print(self.minimax(game, self.search_depth))
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    #need to put self
    def min_value(self,game,d):
           moveset = {}
           d = d + 1
           
           #need tp put self.time_left()
           if self.time_left() < self.TIMER_THRESHOLD:
              raise SearchTimeout()
           #github ans #need to put self to denote minimaxplayer
           if (game.is_winner(self) or game.is_loser(self)) :
               return self.score(game, self)
       
           if (d == self.search_depth):
               return self.score(game, self)

           min_v = float("inf")
           for move in game.get_legal_moves():
               b = game.copy()
               b.apply_move(move)
               v =  self.max_value(game,d)
               if (v < min_v):
                  min_v = v
           return min_v

    #need to put self            
    def max_value(self,game,d):
            d = d + 1
            moveset = {}
            
            if self.time_left() < self.TIMER_THRESHOLD:
              raise SearchTimeout()
            #github ans 
            #github ans #need to put self to denote minimaxplayer
            if (game.is_winner(self) or game.is_loser(self)) :
               return self.score(game.forecast_move(move), self)
           
            if (d == self.search_depth):
               v = self.score(game, self)
               return v
            max_v = -float("inf")
            for move in game.get_legal_moves():
               b = game.copy()
               b.apply_move(move)
               v =  self.min_value(game.forecast_move(move),d)
               if (v > max_v):
                  max_v = v
            return max_v 
      
    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        #if self.time_left() < self.TIMER_THRESHOLD:
          #  raise SearchTimeout()
        
        # TODO: finish this function!
        moveset = {}
      
        if self.time_left() < self.TIMER_THRESHOLD:
              raise SearchTimeout()
        #github ans 
        if (len(game.get_legal_moves())==0):
               return (-1,-1)
        #github ans

        h = -float("inf")  
        d = 0
        for move in game.get_legal_moves():
             moveset[move] = self.min_value(game.forecast_move(move),d)
             if (h < moveset[move]):
                 h = moveset[move]
       
        for move in game.get_legal_moves():
            if (moveset[move] == h):
               return move
        
       
class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        depth = 1
        try:
            best_move = self.alphabeta(game, depth)
            depth = depth + 1
      
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        #github ans 
        #github ans #need to put self to denote alphabetaplayer
        if (game.is_winner(self) or game.is_loser(self)) :
            return self.score(game, self)
        #github ans
        if (depth == 0):
           return self.score(game, self)
        v = -float("inf")
        depth = depth - 1
        for move in game.get_legal_moves():
           val = self.max_value(game.forecast_move(move), depth, alpha, beta)
           if (v < val):
              v = val
           if (beta <= v):
              return v
           if (alpha < v):
               alpha = v
        return v
    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout() 
        
        #github ans 
        #github ans #need to put self to denote alphabetaplayer
        if (game.is_winner(self) or game.is_loser(self)) :
            return self.score(game, self)
        #github ans
        if (depth == 0):
           return self.score(game, self)
        v = float("inf")
        depth = depth - 1
        for move in game.get_legal_moves():
           val = self.max_value(game.forecast_move(move), depth, alpha, beta)
           if (v > val):
              v = val
           if (alpha >= v):
              return v
           if (beta > v):
               beta = v
           
        return v
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
       
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moveset = {}
        depth = depth - 1
        if (len(game.get_legal_moves())==0):
              return (-1, -1)
        v = -float("inf")
        for move in game.get_legal_moves():
            val = self.min_value(game.forecast_move(move),depth,alpha,beta)
            moveset[move] = val
            if (v < val):
               v = val
        for move in game.get_legal_moves():
            if (moveset[move] == v):
                return move


















































           
        """
        # TODO: finish this function!
        def max_value(game,d,depth,alpha,beta):
           moveset = {}
           d = d + 1
           v = 0
           if (len(game.get_legal_moves())==0):
               return (-1,-1)


           for move in game.get_legal_moves():
              if(d == depth):
                 v = custom_score(game, game._active_player)
                 return v

           v = float("inf") 
           for move in game.get_legal_moves():
              b = game.copy()
              b.apply_move(move)
              moveset[move] = min_value(b,d,depth,alpha, beta) 
              if (beta > moveset[move]):
                 beta = moveset[move]
              if (beta < alpha):
                return beta
              if(v > moveset[move]):
                 v = moveset[move]
           alpha = v
           return alpha               

        def min_value(game,d,depth,alpha,beta):
           moveset = {}
           d = d + 1
           v = 0
           if (len(game.get_legal_moves())==0):
               return (-1,-1)

           for move in game.get_legal_moves():
              if(d == depth):
                 v = custom_score(game, game._active_player)
                 return v

           v = float("inf") 
           for move in game.get_legal_moves():
              b = game.copy()
              b.apply_move(move)
              moveset[move] = min_value(b,d,depth,alpha, beta) 
              if (alpha > moveset[move]):
                 alpha = moveset[move]
              if (alpha < beta):
                return alpha
              if(v > moveset[move]):
                 v = moveset[move]
           beta = v
           return beta


        moveset = {}
        d = 0
        if (len(game.get_legal_moves())==0):
               return (-1,-1)

        for move in game.get_legal_moves():
              if(d == depth):
                 v = custom_score(game, game._active_player)
                 if (alpha < v):
                    alpha = v
                 moveset[move] = v
        v = -float("inf") 
        for move in game.get_legal_moves():
            b = game.copy()
            b.apply_move(move)
            moveset[move] = max_value(b,d,depth,alpha, beta) 
            if (alpha > moveset[move]):
                 alpha = moveset[move]
            if(v < moveset[move]):
               v = moveset[move]

        beta = v
        for move in game.get_legal_moves():
             if (moveset[move] == beta):
                return move
"""
            
