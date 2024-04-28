from Card import Hand, Deck
import random


class PokerHand(Hand):
    """Represents a poker hand."""

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.
        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
        
    def rank_hist(self):
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1
        return self.ranks

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
        """
        self.suit_hist()
        flag = False
        for val in self.suits.values():
            if val >= 5:
                flag = True
        if flag:
            return True
        return False

    def has_pair(self):
        """Returns True if the hand has a pair, False otherwise.
        """
        self.rank_hist()
        flag = False
        for val in self.ranks.values():
            if val == 2:
                flag = True
        if flag:
            return True
        return False

    def has_twopair(self):
        """Returns True if the hand has two pairs, False otherwise.
        """
        self.rank_hist()
        counter = 0
        for val in self.ranks.values():
            if val == 2:
                counter += 1
        return counter == 2

    def has_triple(self):
        """Returns True if the hand has a triple, False otherwise.
        """
        self.rank_hist()
        flag = False
        for val in self.ranks.values():
            if val == 3:
                flag = True
        if flag:
            return True
        return False

    def has_care(self):
        """Returns True if the hand has a care, False otherwise.
        """
        self.rank_hist()
        flag = False
        for val in self.ranks.values():
            if val==4:
                flag = True
        if flag:
            return True
        return False

    def has_full_house(self):
        """Returns True if the hand has a full_house, False otherwise.
        """
        if self.has_pair() and self.has_triple():
            return True
        return False

    def has_streat(self):
        """Returns True if the hand has a streat, False otherwise.
        """
        self.rank_hist()
        lst = sorted(self.ranks.keys())
        counter = 0
        for index, value in enumerate(lst):
            if index+1<len(lst) and value-lst[index+1]==-1:
                counter+=1
        if counter==len(lst)-1:
            return True
        return False

    def has_streat_flush(self):
        """Returns True if the hand has a streat flush, False otherwise.
        """
        if self.has_streat() and self.has_flush():
            return True
        return False
    
    def determine_comb(self):
        """Determins the biggest combination in the hand"""
        comb_dict_rate = dict(zip([1, 2, 3, 4, 5, 6, 7, 8], [self.has_pair(), self.has_twopair(), self.has_triple(), self.has_streat(), self.has_flush(), self.has_full_house(), self.has_care(), self.has_streat_flush()]))
        comb_list = ['pair', 'two pair', 'triple', 'streat', 'flush', 'full house', 'care', 'streat flush']
        res = 0
        for i in comb_dict_rate.keys():
            if comb_dict_rate[i] == True:
                res = max(i, res)
        if res:
            return f'{comb_list[res-1]}', res
        else:
            return f'no comb', res
        

class MyHand(PokerHand):
    """Represents the hand of the real player. The same class PokerHand but with another identity
    """
    pass


class GameSession():

    """Rule the session of the game:
        self.deck: the deck used in the game
        self.coefs: coeficients of the combinations
        self.bank: the bank of the game, collects all the paris
        self.players: the list of players. list[PokerHand]
        self.players_names: list of names of players
        self.players_combos: the dictionsry of combinations of players
        self.wins: the dictionary of wins of every player
    """

    def __init__(self) -> None:
        self.deck = self.create_deck()
        self.coefs = dict(zip([0, 1, 2, 3, 4, 5, 6, 7, 8], 
        [0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]))
        self.bank = 0
        self.players = []
        self.players_names = []
        self.players_combos = None
        self.wins = None


    def prepare_game_session(self): 
        '''Preparing the game session (n players are with certain number of cards)
        '''
        self.create_deck()
        self.create_players()
        print('All is compleated') 


    def create_deck(self):  
        '''Create of a deck with 56 cards
        '''
        self.deck = Deck()
        self.deck.shuffle()


    def create_players(self, n=3):   
        '''Create n players 
        '''
        for _ in range(n):
            player = PokerHand()
            self.players.append(player)
        self.players_names = [i.label for i in self.players]
        print('task create_players has finished')
        print(f'Players {" ".join(self.players_names)}')


    def give_cards(self, number=7):     
        '''Gives certain number of cards to all players
        '''
        for player in self.players:
            self.deck.move_cards(player, number)


    def make_init_pari(self, pari=25):
        """Makes each player make the initial pari
        """
        for player in self.players:
            self.bank += pari
            player.coins[pari] -= 1
            player.count_balance()


    def find_combs(self):
        """Finds a combination, initialise and fill the dictionary self.players_combos
        """
        self.players_combos = {}
        for player in self.players:
            comb = player.determine_comb()
            self.players_combos[player] = comb

        #return self.show_combs(lst_of_combs=combs_list)


    def make_paris(self):
        """Makes each player pake pari depends on his/her combination
        """
        paris_list = []
        for key, value in self.players_combos.items():
            if isinstance(key, MyHand):
                lst = list(map(lambda a: a.__str__(), key.cards))
                string = '\n'.join(lst)
                paris_list.append((f'{key.label}, you have got these cards, find the highest comb and make your pari:\n', string))
                continue
            else:
                coef = self.coefs[value[1]]
                pari = key.total_balance * coef
                paris_list.append((key.label, pari))
                key.total_balance -= pari
                self.bank += pari

        return self.show_paris(paris_list)


    def show_paris(self, paris_list):
        """Compose the massage which consists of name of player and his pari
        """
        result = ''
        for player in paris_list:
            result += f'{player[0]} - {player[1]}\n\n'
        
        return result


    def show_combs(self):
        """Compose the massage which consists of the cards and the combination
        """
        result = 'So, the results of the round:\n'
        for player, combo in self.players_combos.items():
            result += f'{player} - {combo[0]}\n\n'

        return result


    def determine_winners(self):
        """Determins the winners of the round
        """
        winners = []
        coefs_of_combs = [i[1] for i in self.players_combos.values()]
        maximum = max(coefs_of_combs)
        for player, combo in self.players_combos.items():
            self.deck.cards.extend(player.cards)
            self.deck.shuffle()
            player.cards.clear()
            if combo[1] == maximum:
                winners.append(player)
                self.wins[player] += 1

        number = len(winners)
        price = self.bank//number
        self.bank *= 0

        for player in winners:
            player.total_balance += price

        result = list(map(lambda x: x.label, winners))
        return f'{" ".join(result)} win this round!'


    def determine_losers_and_final_winner(self):
        """Determins the losers and final winner
        """
        result = '-'
        index = 0
        while index<len(self.players):
            if self.players[index].total_balance <= 0:
                if isinstance(self.players[index], MyHand):
                    self.players.pop(index)
                    result += f'You cant continue because you havent got enough money!\n'
                else:
                    self.players.pop(index)
                    result += f'{self.players[index].label} has quited the game bacause his balance is 0\n'
            else:
                index += 1
                
        try:    #Player can quit the game in his reason
            if self.wins[self.players[0]] == 0 and max(self.wins.values()) == 2:
                self.players.pop(0)
                result += f'{self.players[0].label} is not in a good mood today, he/she has lost 2 times in a row and dont want play more\n'

            if self.players[1].total_balance <= 3000:
                self.players.pop(1)
                result += f'{self.players[1].label} is not very ardent, so having lost {5000-self.players[1].total_balance} he/she is leaving the game\n'

            if random.randint(1, 10) == 3:
                self.players.pop(2)
                result += f"The {self.players[2]}'s father has come to punish him/her for losing their money in pocker\n"
        except IndexError:
            pass

        if len(self.players) == 1:
            result += f'{self.players[0]} HAS WON THIS GAME WITH TOTAL PRICE {self.players[0].total_balance}\n'

        return result
