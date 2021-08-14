import itertools
import random
from copy import deepcopy
from operator import attrgetter
from typing import (Counter,
                    Iterable,
                    Iterator,
                    List,
                    NamedTuple,
                    NewType,
                    Sequence,
                    Set,
                    Tuple,
                    TypeVar)
 
Card = NewType('Card', str)
Hand = Counter[Card]
Deck = Tuple[Card, ...]
Watchlist = Set[Card]
T = TypeVar('T')
 
SUITS_COUNT = 4
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
DECK = RANKS * SUITS_COUNT
 
EMPTY_HAND_MESSAGE = "{} is without cards. They go fishing."
CARD_REQUEST_MESSAGE = "{player_name} asks for {card}"
NO_CARD_MESSAGE = "{player_name} doesn't have {card}"
BOOK_COMPLETED_MESSAGE = "{player_name} completed the book of {card}'s."
FISHING_RESULT_MESSAGE = "{player_name} fished a {card}"
 
 
class Player(NamedTuple):
    name: str
    hand: Hand
    is_human: bool
    score: int = 0
    is_lucky: bool = True  # if False, turn goes to another player
    watchlist: Watchlist = set()  # used by AI to track enemy's cards
 
 
def play(deck: Deck = DECK,
         *,
         first_hand_count: int = 9,
         lucky_fishing: bool = False) -> None:
    """
    Plays the Go Fish game according to
    http://www.rosettacode.org/wiki/Go_Fish
    :param deck: deck from where the cards are drawn
    :param first_hand_count: starting amount of cards for a player
    :param lucky_fishing: if True, continue playing
    after fishing the card from the deck
    that was asked from an opponent
    """
    deck = shuffle(deck)
    deck, (hand, other_hand) = deal_first_hands(deck, count=first_hand_count)
    human = Player(name=input('Name yourself: '),
                   hand=hand,
                   is_human=True)
    ai = Player(name='Computer',
                hand=other_hand,
                is_human=False)
    human = check_hand_for_books(human)
    ai = check_hand_for_books(ai)
 
    player, opponent = ai, human
    for turn in itertools.count(1):
        player, opponent = opponent, player
        print_turn_stats(turn=turn,
                         players=(player, opponent),
                         cards_left=len(deck))
        while cards_in_game(deck, hands=(player.hand, opponent.hand)):
            player, opponent, deck = play_turn(player,
                                               opponent,
                                               deck,
                                               lucky_fishing=lucky_fishing)
            if not player.is_lucky:
                break
        else:
            print_final_stats((player, opponent))
            return
 
 
def shuffle(deck: Deck) -> Deck:
    """Returns a shuffled deck"""
    deck = list(deck)
    random.shuffle(deck)
    return tuple(deck)
 
 
def deal_first_hands(deck: Deck,
                     count: int) -> Tuple[Deck, Tuple[Hand, Hand]]:
    """Gives count cards to each player"""
    hands = (Hand(), Hand())  # type: Tuple[Hand, Hand]
    for hand in ncycles(hands, count):
        card, deck = fish(deck)
        hand[card] += 1
    return deck, hands
 
 
def fish(deck: Deck) -> Tuple[Card, Deck]:
    """Returns a fished card from a deck, and a new deck"""
    return deck[-1], deck[:-1]
 
 
def ncycles(iterable: Iterable[T], n: int) -> Iterator[T]:
    """Returns the sequence elements n times"""
    repeat = itertools.repeat(tuple(iterable), n)
    return itertools.chain.from_iterable(repeat)
 
 
def check_hand_for_books(player: Player) -> Player:
    """
    Walks through cards in the hand,
    removes books and adds corresponding score
    """
 
    def is_book(card_and_count: Tuple[Card, int]) -> bool:
        """
        For a pair of card-count
        checks if count equals the number of suits
        """
        return card_and_count[1] == SUITS_COUNT
 
    player = deepcopy(player)
    cards_counts = player.hand.items()
    books = list(filter(is_book, cards_counts))  # type: List[Tuple[Card, int]]
    for card, _ in books:
        player.hand.pop(card)
    return player._replace(score=player.score + len(books))
 
 
def print_turn_stats(*,
                     turn: int,
                     players: Sequence[Player],
                     cards_left: int) -> None:
    """Prints stats of the current turn"""
    name_score = name_score_pairs(players, sep=' ')
    print(f'\nTurn {turn} ({name_score}) {cards_left} cards remaining.')
 
 
def name_score_pairs(players: Sequence[Player],
                     *,
                     sep: str) -> str:
    """Returns a string of pairs of 'name: score'; human goes first"""
    players = sorted(players,
                     key=attrgetter('is_human'),
                     reverse=True)
    name_score_generator = map('{0.name}: {0.score}'.format, players)
    return sep.join(name_score_generator)
 
 
def cards_in_game(deck: Deck,
                  hands: Iterable[Hand]) -> bool:
    """Checks if hands or the deck have any cards"""
    return deck or any(hands)
 
 
def play_turn(player: Player,
              opponent: Player,
              deck: Deck,
              *,
              lucky_fishing: bool) -> Tuple[Player, Player, Deck]:
    """Plays one turn"""
    player, deck = replenish_card(player, deck=deck)
    opponent, deck = replenish_card(opponent, deck=deck)
 
    if player.is_human:
        requested_card, watchlist = human_asks_card(
            hand=player.hand,
            watchlist=opponent.watchlist)
        opponent = opponent._replace(watchlist=watchlist)
    else:
        requested_card = ai_asks_card(player)
 
    if requested_card in opponent.hand:
        player, opponent = correct_guess_actions(player=player,
                                                 opponent=opponent,
                                                 card=requested_card)
    else:
        player, deck = wrong_guess_actions(
            player=player,
            opponent=opponent,
            requested_card=requested_card,
            deck=deck,
            lucky_fishing=lucky_fishing)
    return player, opponent, deck
 
 
def print_final_stats(players: Sequence[Player]) -> None:
    """Prints final stats"""
    name_score = name_score_pairs(players, sep='\n')
    print(f'\nScores: \n{name_score}\n')
    scores = list(map(attrgetter('score'), players))
    if all(score == scores[0] for score in scores):
        print('Draw!')
    else:
        winning_player = max(players, key=attrgetter('score'))
        print(winning_player.name, 'won!')
 
 
def replenish_card(player: Player,
                   *,
                   deck: Deck) -> Tuple[Player, Deck]:
    """Returns a player with a card drawn from a deck"""
    player = deepcopy(player)
    if not player.hand:
        print(EMPTY_HAND_MESSAGE.format(player.name))
        card, deck = fish(deck)
        player.hand[card] += 1
        print_fishing_result(player=player,
                             card=card)
    return player, deck
 
 
def human_asks_card(*,
                    hand: Hand,
                    watchlist: Watchlist) -> Tuple[Card, Watchlist]:
    """Set of actions for when human asks a card from computer"""
    watchlist = watchlist.copy()
    print_hand(hand)
    requested_card = ask_for_card(hand=hand)
    watchlist.add(requested_card)
    return requested_card, watchlist
 
 
def ai_asks_card(player: Player) -> Card:
    """Set of actions for when computer asks a card from human"""
    requested_card = request_card(player.hand,
                                  watchlist=player.watchlist)
    print_message(CARD_REQUEST_MESSAGE,
                  player_name=player.name,
                  card=requested_card)
    return requested_card
 
 
def correct_guess_actions(player: Player,
                          opponent: Player,
                          card: Card):
    """
    Set of actions for when player guesses correctly card
    in a hand of an opponent
    """
    player = deepcopy(player)
    opponent = deepcopy(opponent)
    card_count = opponent.hand.pop(card)
    print(f'{player.name} got {card_count} more {card} '
          f'from {opponent.name}.')
    player.hand[card] += card_count
    player = check_book(player, card)
    if not player.is_human:
        player.watchlist.discard(card)
    player = player._replace(is_lucky=True)
    return player, opponent
 
 
def wrong_guess_actions(*,
                        player: Player,
                        opponent: Player,
                        requested_card: Card,
                        deck: Deck,
                        lucky_fishing: bool) -> Tuple[Player, Deck]:
    """
    Set of actions for when player guesses incorrectly card
    in a hand of an opponent.
    `lucky_fishing` determines if player can continue playing
    after fishing the wanted card
    """
    player = deepcopy(player)
    print_message(NO_CARD_MESSAGE,
                  player_name=opponent.name,
                  card=requested_card)
    card, deck = fish(deck)
    player.hand[card] += 1
    print_fishing_result(player=player,
                         card=card)
    player = check_book(player, card)
    if lucky_fishing:
        player = player._replace(is_lucky=card == requested_card)
    else:
        player = player._replace(is_lucky=False)
    if player.is_lucky:
        print("What a luck! "
              "The fished card was the same as requested!")
    return player, deck
 
 
def print_hand(hand: Hand) -> None:
    """Prints a hand in the following form: 'Q Q 7 7 7 3'"""
    ranks = itertools.starmap(itertools.repeat, hand.items())
    print(*itertools.chain.from_iterable(ranks))
 
 
def ask_for_card(hand: Hand) -> Card:
    """Asks user for a card, and checks if it is in their hand"""
    while True:
        asked_card = Card(input('What card do you ask for? '))
        if asked_card in hand:
            return asked_card
        print("You don't have that card. Try again!")
 
 
def request_card(hand: Hand, watchlist: Watchlist) -> Card:
    """AI-like choice for a card that will be asked from a human"""
    candidates = list(watchlist & set(hand.keys()))
    if not candidates:
        candidates = list(hand.keys())
    return random.choice(candidates)
 
 
def print_message(message: str,
                  *,
                  player_name: str,
                  card: str) -> None:
    """Prints a template message"""
    print(message.format(player_name=player_name,
                         card=card))
 
 
def check_book(player: Player,
               card: Card) -> Player:
    """
    Checks if player has all cards of specified type,
    removes them if true, and adds +1 to score
    """
    player = deepcopy(player)
    if player.hand[card] == SUITS_COUNT:
        print_message(BOOK_COMPLETED_MESSAGE,
                      player_name=player.name,
                      card=card)
        player.hand.pop(card)
        player = player._replace(score=player.score + 1)
    return player
 
 
def print_fishing_result(*,
                         player: Player,
                         card: Card) -> None:
    """
    Prints result of fishing.
    Showing card or not depends on if a player is a human.
    """
    card_stub = str(card) if player.is_human else 'card'
    print_message(FISHING_RESULT_MESSAGE,
                  player_name=player.name,
                  card=card_stub)
 
 
if __name__ == "__main__":
    play()
