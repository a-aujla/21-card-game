# Player and Table class for simplified 21 card game
# Author: Amrit Aujla
# References: lecture slides and labs from CMPUT 175
# Collaborators: None


from playingCards import Card, Deck

class Player:
    # class for Player in simplified 21 Card game
    
    def __init__(self):
        '''
        Initializes the Player class.
        
        Inputs: 
            self is the Player to initalize.
        
        Returns: None
        '''
        # create attributes
        self.__hand = []
        self.__value = 0
        self.__cards = 0
        
        
    def addToHand(self, card):
        '''
        Adds the card to the player’s hand after asserting that it is a Card instance. 
        
        Inputs:
            self is the Player to add cards to.
            card (Card): the card to add.
        
        Returns: None
        '''
        # assert it is card instance and add card to hand
        assert isinstance(card, Card), 'card must be Card instance'
        self.__hand.append(card)
        self.__value += card.getValue()
        self.__cards += 1
        
        
    def clearHand(self):
        '''
        Removes any cards in the player’s hand and resets the value to 0.
        
        Inputs: 
            self is the Player whose hand is being cleared.
        
        Returns: A list of the cards that were removed from the player’s hand.
        '''
        removed_cards = []
        
        # remove all cards
        for i in range(self.__cards):
            removed_cards.append(self.__hand.pop())
        
        self.__cards = 0
        self.__value = 0
        return removed_cards
    
    
    def getHandValue(self):
        '''
        Returns the current value (an integer) of the player’s hand.
        
        Inputs:
            self is the Player whose hand value is being returned.
        '''
        # return value
        return self.__value
    
    
    def revealAllCards(self):
        '''
        Turns over any cards that are face down in a player’s hand so that all cards are face up.
        
        Inputs: 
            self is the Player whose cards are being revealed.
        
        Returns: None
        '''
        # Turn over card if not face up
        for card in self.__hand:
            if not card.isFaceUp():
                card.turnOver()
                
    
    def __str__(self):
        '''
        Returns the string representation of the Player instance.
        The string includes information about what cards are in the hand, if all cards are facing up, and the value of the hand.
        
        Inputs: 
            self is the Player to return a string for.
        '''
        all_face_up = True
        string = 'hand:'
        
        # add cards to string
        for card in self.__hand:
            if not card.isFaceUp():
                all_face_up = False
            string += str(card)
            
        # check if hand is empty and add value if all face up
        if self.__value == 0:
            string += ' value = 0'
        elif all_face_up:
            string += ', value = %d' % self.__value
    
        return string
    
    
    
class Table():
    # class for Table in simplified 21 card game
    
    def __init__(self):
        '''
        Initializes the table class.
        
        Inputs:
            self is the Table to initialize.
            
        Returns: None
        '''
        # create attributes
        self.__player = Player()
        self.__dealer = Player()
        self.__deck = Deck()
        self.__discard = []
    
    
    def dealHands(self):
        '''
        Deals the first four cards from the front of the deck to the player and dealer.
        The first and third cards are dealt face up to the player. 
        The second and fourth cards are dealt to the dealer face up and face down respectively.
        
        Inputs:
            self is the Table to deal cards to
            
        Returns: None
        '''
        player_order = [self.__player, self.__dealer, self.__player]
        
        # add face up cards to player/dealer hands
        for player in player_order:
            player.addToHand(self.__deck.deal())
        
        # add face down card to dealer hand
        card = self.__deck.deal()
        card.turnOver()
        self.__dealer.addToHand(card)
        
    
    def playerHit(self):
        '''
        Deals a card from the front of the deck to the player, face up.
        If the deck runs out of cards, the deck is repopulated using the cards from the discard pile.
        
        Inputs:
            self is the Table
            
        Returns (bool): whether the player has gone bust with the new card (True) or not (False).
        '''
        card_added = False
        
        # try to add card or repopulate if deck empty
        while not card_added:
            try:
                card = self.__deck.deal()
                self.__player.addToHand(card)
                card_added = True
            except:
                self.__deck.repopulate(self.__discard)
            
        # return if player has gone bust
        if self.__player.getHandValue() > 21:
            return True
        else:
            return False

    
    def dealerHit(self):
        '''
        Turns the dealer’s second card over and displays the value of the current hand.
        Continues to deal face up cards to dealer as long as the value of the dealer’s hand is 16 or less.
        If the deck runs out of cards, the deck is repopulated using the cards from the discard pile.
        
        Inputs:
            self is the Table.
            
        Returns (bool): Whether the dealer has gone bust (True) or not (False).
        '''
        # display dealer's cards
        self.__dealer.revealAllCards()
        print(self)
        
        while self.__dealer.getHandValue() <= 16:
            
            # try to add cards from deck
            try:
                self.__dealer.addToHand(self.__deck.deal())
                print('Dealer must take card...')
                print(self)
            
            # repopulate deck if empty
            except:
                self.__deck.repopulate(self.__discard)
        
        # check if dealer went bust    
        if self.__dealer.getHandValue() > 21:
            print("Dealer went bust.", end=' ')
            return True
        elif self.__dealer.getHandValue() == 21:
            print("Dealer has a natural 21!", end=' ')
            return False
        else:
            return False

    
    def playerNatural(self):
        '''
        Returns True if the value of the player’s hand is exactly 21, False otherwise.
        
        Inputs:
            self is the Table.
        '''
        # check if player hand is 21
        if self.__player.getHandValue() == 21:
            return True
        else:
            return False
    
    
    def whoWon(self):
        '''
        Compares the player’s and dealer’s hands to determine who wins and displays message.
        
        Inputs:
            self is the Table
            
        Returns: None
        '''
        # find how close to 21 both are
        player_difference = 21 - self.__player.getHandValue()
        dealer_difference = 21 - self.__dealer.getHandValue()
        
        # check who is closer
        if player_difference > dealer_difference:
            print('Dealer wins', end=' ')
        elif player_difference == dealer_difference:
            print('Tie! No one wins', end=' ')
        else:
            print('Player wins', end=' ')
    
    
    def clearTable(self):
        '''
        Removes all cards from the player’s and dealer’s hands, and adds those cards to the discard pile.
        
        Inputs:
            self is the Table
            
        Returns: None
        '''
        # remove from hand and add to discard
        self.__discard.extend(self.__player.clearHand())
        self.__discard.extend(self.__dealer.clearHand())
        
        
    def __str__(self):
        '''
        Returns the string representation of the Table instance. 
        The string contains information about the player’s hand and the dealer’s hand.
        
        Inputs:
            self is the Table
            
        Returns: None
        '''
        string = "Player's %s\nDealer's %s" % (str(self.__player), str(self.__dealer))
        return string
        
        
        
def player_test():
    '''
    Tests for the player class
    
    Inputs: N/A
    
    Returns: None
    '''
    player = Player()
    deck = Deck()
    
    # Add cards to player's hand
    for i in range(5):
        player.addToHand(deck.deal())
    print("\nAfter adding 5 cards: %s\n" % player)
    
    print("The player's hand value is: %d\n" % player.getHandValue())
    
    # show all cards
    player.revealAllCards()
    print("After revealing cards: %s\n" % player)
    
    # clear player's hand
    cleared_cards = player.clearHand()
    print("After clearing: %s" % player)
    print("The player's hand value is %d" % player.getHandValue())
    print('The cleared cards are: ', end='')
    for card in cleared_cards:
        print(card, end='')
    
    
def table_test():
    '''
    Tests for the table class.
    
    Inputs: N/A
    
    Returns: None
    '''
    table = Table()
    print(table)
    print('-' * 100)
    table.dealHands()
    print(table)
    print('-' * 100)
    #bust = table.playerHit()
    #print(bust)
    #print(table)
    #print('-' * 100)
    #table.dealerHit()
    #for i in range(48):
        #table.playerHit()
    #table.clearTable()
    #table.playerHit()
    #print(table)
    #table.dealerHit()
    #print(table)
    table.clearTable()
    table.dealHands()
    print(table)
    table.dealerHit()
    table.clearTable()
    table.dealHands()
    print(table)
    table.whoWon()
    
if __name__ == "__main__":
    player_test()
    #table_test()
