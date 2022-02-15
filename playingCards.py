# Card and Deck classes for simplified 21 card game.
# Author: Amrit Aujla
# References: lecture slides and previous labs
# Collaborators: None


from queues import CircularQueue
import random


class Card:
    # Each instance of this class represents a playing card.
    
    def __init__(self, code, faceUp):
        '''
        Initializes the card class.
        
        Inputs:
            code (str): Two characters represent the rank and suit of the card respectively.
            faceUp (bool): True if card is facing up; False otherwise.
            
        Returns: None
        '''
        # check input
        assert code[0].upper() in 'A23456789TJQK', 'Error: rank is not valid.'
        assert code[1].upper() in 'CDHS', 'Error: suit is not valid.'
        assert isinstance(faceUp, bool), 'Error: faceUp must be True or False'
        
        # create attributes
        self.__rank = code[0].upper()
        self.__suit = code[1].upper()
        self.__faceUp = faceUp
        
    
    def getRank(self):
        '''
        Returns the single string character representing the rank of the Card instance.
        
        Inputs:
            self is the Card.
        '''
        # return rank
        return self.__rank
    
        
    def getSuit(self):
        '''
        Returns the single string character representing the suit of the Card instance.
        
        Inputs:
            self is the Card.
        '''
        # return suit
        return self.__suit
        
        
    def getValue(self):
        '''
        Returns the integer value of the Card instance according to its rank.
        
        Inputs:
            self is the Card.
        '''
        # find and return integer value of rank
        if self.__rank == 'A':
            return 1
        elif self.__rank in 'TJQK':
            return 10
        else:
            return int(self.__rank)
        
    
    def isFaceUp(self):
        '''
        Returns the Boolean value indicating whether the Card instance is facing up or down.
        
        Inputs:
            self is the Card.
        
        Returns: True if the card is facing up or False if the card is facing down.
        '''
        # return True or False
        return self.__faceUp
        
        
    def turnOver(self):
        '''
        Updates the Card instance so that if it was previously facing up, it will now face down. And if it was
        previously facing down, it will now face up.
        
        Inputs:
            self is the Card.
        
        Returns: None
        '''
        # update the card instance
        if self.__faceUp == True:
            self.__faceUp = False
        else:
            self.__faceUp = True
        
        
    def __str__(self):
        '''
        Returns the string representation of the Card instance. 
        
        Inputs:
            self is the Card.
        '''
        # check if card is faceup and return string
        if self.__faceUp:
            return '[ %s%s ]' % (self.getRank(), self.getSuit())
        else:
            return '[ xx ]'
        
        
        
class EmptyDeckException(Exception):
    # Subclass of Exception class.
    
    def __init__(self):
        '''
        Initializes the EmptyDeckException class
        
        Inputs:
            self is the EmptyDeckException
            
        Returns: None
        '''
        self.args = ("Cannot deal card from an empty deck.", )



class Deck:
    # Deck made up of cards from the Card class.
    
    def __init__(self):
        '''
        Initializes the Deck class. Reads a file and adds cards from that file to the Deck.
        
        Inputs:
            self is the Deck.
        
        Returns: None
        '''
        self.__deck = CircularQueue(52)
        
        # ask for filename until valid
        file_valid = False
        while not file_valid:
            try:
                filename = input('Name of file that should be used to populate the deck of cards: ')
                file = open(filename, 'r')
                file_valid = True
        
                # check for duplicate cards
                cards = {}
                for line in file:
                    card = line.strip('\n')
                    if card in cards.keys():
                        raise Exception('Cannot populate deck: invalid data in %s' % filename)
                    cards[card] = 1
                    
                    # check if card is valid
                    try:
                        card = Card(card, False)
                        self.__deck.enqueue(card)
                    except AssertionError:
                        raise Exception('Cannot populate deck: invalid data in %s' % filename)
                
                # check if deck has 52 cards
                if not self.__deck.isFull():
                    self.__deck.clear()
                    raise Exception('Cannot populate deck: invalid data in %s' % filename)
             
            # handle exceptions and close file 
            except OSError:
                print('Cannot read from %s.' % filename)      
            except Exception:
                file.close()
                raise
            else:
                file.close()

    
    def deal(self):
        '''
        Modifies the deck by removing the card from the front of the deck.
        
        Inputs: N/A.
        
        Returns: The front Card face up.
        '''
        # check if deck contains cards before returning
        if self.__deck.isEmpty():
            raise EmptyDeckException
        front_card = self.__deck.dequeue()
        front_card.turnOver()
        return front_card
            
    
    def repopulate(self, cardList):
        '''
        Displays a message that the deck is being repopulated and modifies the deck by adding cards to it.
        
        Inputs:
            cardList (list): List of cards to be added to the deck in a random order.
        
        Returns: None.
        '''
        # shuffle and add cards
        print('Repopulating deck with cards...')
        random.shuffle(cardList)
        for card in cardList:
            if card.isFaceUp():
                card.turnOver()
            self.__deck.enqueue(card)
    
    
    def __str__(self):
        '''
        Returns the string representation of the Deck instance.
        
        Inputs: N/A
        '''
        string = 'front --> '
        row_count = 0
        row_length = 13
        
        for i in range(self.__deck.size()):
            
            # make rows of 13
            if row_count == row_length:
                string += '\n' + ' ' * 10
                row_count = 0
                
            # take card from deck face up
            card = self.__deck.dequeue()
            if not card.isFaceUp():
                card.turnOver()
                
            # add cards to string and return to deck
            string += ' %s' % (card)
            row_count += 1
            self.__deck.enqueue(card)
            
        string += ' <-- back'
        
        return string
    


def card_tests():
    '''
    Tests for card class
    
    Inputs: N/A
    
    Returns: None
    '''
    # create card and test it
    myCard = Card('AH', True)
    print('My card is', myCard)
    
    is_pass = (myCard.getRank() == 'A')
    assert is_pass == True, "fail the test"
    
    is_pass = (myCard.getSuit() == 'H')
    assert is_pass == True, "fail the test"    
    
    is_pass = (myCard.getValue() == 1)
    assert is_pass == True, "fail the test"
    
    is_pass = (myCard.isFaceUp() == True)
    assert is_pass == True, "fail the test"    
            
    myCard.turnOver()
    
    is_pass = (myCard.isFaceUp() == False)
    assert is_pass == True, "fail the test"     
    
    print('My turned over card is', myCard)
    
    # test second card
    myCard = Card('JS', False)
    print('My new card is', myCard)
    
    is_pass = (myCard.getRank() == 'J')
    assert is_pass == True, "fail the test"
    
    is_pass = (myCard.getSuit() == 'S')
    assert is_pass == True, "fail the test"    
    
    is_pass = (myCard.getValue() == 10)
    assert is_pass == True, "fail the test"
    
    # test third card
    myCard = Card('9S', False)
    
    is_pass = (myCard.getValue() == 9)
    assert is_pass == True, "fail the test"    
    
    
def deck_tests():
    '''
    Tests for the deck class.
    
    Inputs: N/A
    
    Returns: None
    '''
    print('')
    deck = Deck()
    print('\n%s' % deck)
    
    # create empty list for cards dealt
    cards_dealt = []
    card = deck.deal()
    cards_dealt.append(card)
    
    # Deal 1 card
    print('\nCard dealt:', card)
    card.turnOver()
    print('Card dealt:', card)
    print('\nDeck after dealing card:\n%s' % deck)
    
    # Deal 10 cards
    for i in range(10):
        card = deck.deal()
        cards_dealt.append(card)
    print('\nDeck after dealing 10 more cards:\n%s\n' % deck)
    
    # repopulate deck using cards dealt
    deck.repopulate(cards_dealt)
    cards_dealt.clear()
    print(deck)



if __name__ == "__main__":
    card_tests()
    deck_tests()