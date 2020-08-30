import time
from typing import Dict, Any

K_VALUE = 32


class Player:
    """
    Player object that contains player history, rating and name
    """
    rating: int
    name: str
    match_history: Dict[str, Any]

    def __init__(self, player_name: str, elo: int = 1000):
        """
        Creates a player object
        :param elo: rating of the player, default is 1000
        :param player_name: name of the player as a string
        """
        self.rating = elo
        self.name = player_name
        self.match_history = {}


class Match:
    """
    Match object for player match history
    """
    winner: str
    loser: str
    player_elo: Dict[str, int]
    expected_win_percent: Dict[str, float]

    def __init__(self, winning_player: Player, losing_player: Player):
        """
        Creates a match object and updates each players elo
        :param winning_player: player object that will win
        :param losing_player: player object that will lose
        """
        self.winner = winning_player.name
        self.loser = losing_player.name
        self.player_elo = {"Winning Player Starting ELO": winning_player.rating,
                           "Losing Player Starting ELO": losing_player.rating}
        winner_win_percent: float = win_percent(winning_player.rating, losing_player.rating)
        rating_change: int = find_rating_change(winner_win_percent)
        winning_player.rating = winning_player.rating + rating_change
        losing_player.rating = losing_player.rating - rating_change
        self.player_elo["Winning Player Final ELO"] = winning_player.rating
        self.player_elo["Losing Player Final ELO"] = losing_player.rating
        self.expected_win_percent = {"Winning Player Expected Win Rate": winner_win_percent,
                                     "Losing Player Expected Win Rate": 1 - winner_win_percent}


def win_percent(player1_elo: int, player2_elo: int) -> float:
    """
    Calculates the chance of player one winning a match given two elo ratings
    :param player1_elo: player one elo int
    :param player2_elo: player two elo int
    :return: chance of player 1 to win
    """
    transformed_elo_1: float = pow(10, player1_elo / 400)
    transformed_elo_2: float = pow(10, player2_elo / 400)
    player_one_win_percent: float = transformed_elo_1 / (transformed_elo_1 + transformed_elo_2)
    return int(player_one_win_percent * 100) / 100


def find_rating_change(player_win_percent: float) -> int:
    """
    Takes a win percentage and returns an elo change that is weighted by the k value
    :param player_win_percent: chance of player winning
    :return: elo change based on win percent and k value which is the weight of any given match
    """
    change: int = round((1 - player_win_percent) * K_VALUE)
    return change


def play_match(winning_player: Player, losing_player: Player) -> None:
    """
    Creates a match object and adds it to each players match history
    :param winning_player: takes a player object that will be the winner
    :param losing_player:  takes a player object that will be the loser
    """
    match_data = Match(winning_player, losing_player).__dict__
    time_data = time.asctime(time.localtime(time.time()))
    winning_player.match_history[time_data] = match_data
    losing_player.match_history[time_data] = match_data
