# Simplified 21 Card Game
# Author: Amrit Aujla
# References: lecture slides and labs from CMPUT 175
# Collaborators: None


from simple21 import Table


def main():
    
    # check if file is valid
    try:
        table, round_num = start_game()
    except Exception as err:
        print(err)
    else:
        continue_game = True
        while continue_game:
            round_num = start_round(table, round_num)
            player_bust, player_natural = player_turn(table)
            who_wins(table, round_num, player_bust, player_natural)
            continue_game = play_again()
    finally:
        goodbye_msg()


def start_game():
    '''
    Starts game by displaying title, creating table and the starting round number.
    
    Inputs: N/A
    
    Returns: 
        table: the Table instance created.
        round_num (int): The round number.
    '''
    # Display title
    title = 'Welcome to CARD GAME 21'
    border = '=' * len(title)
    print(border + '\n' + title + '\n' + border)
    
    # Create table and round number
    table = Table()
    round_num = 0
    
    return table, round_num
    
    
def start_round(table, prev_round):
    '''
    Starts round by dealing cards and updates round number.
    
    Inputs: 
        table (Table): The table with the player and dealer where cards are being dealt.
        prev_round (int): The previous round number.
        
    Returns: current_round (int): The current round number.
    '''
    # update round number and deal hands
    current_round = prev_round + 1
    print("\nDealing cards to player and dealer...")
    table.dealHands()
    print(table)
    
    return current_round


def player_turn(table):
    '''
    Asks player to hit or stay until their turn is over.
    
    Inputs:
        table (Table): table with the player
    
    Returns:
        player_bust (bool): True of player went bust; False otherwise
        player_natural (bool): True if player won; False otherwise
    '''
    # ask player to hit or stay until their turn is over
    player_turn = True
    hit_count = 0
    while player_turn:
        hit = input("Would you like to HIT (H/h) or STAY (S/s)? >> ")
        
        # hit player or stay
        if hit[0].lower() == 'h':
            hit_count += 1
            player_bust = table.playerHit()
            player_natural = table.playerNatural()
            print(table)
            
            # check if player went bust
            if player_bust:
                player_turn = False
        
        else:
            player_turn = False
    
    # make sure bool is being returned
    if hit_count == 0:
        player_bust = False
        player_natural = False

    return player_bust, player_natural
    

def who_wins(table, round_num, player_bust, player_natural):
    '''
    Prints message if player has already won; otherwise continues with dealer's turn and displays
    who won at the end of it. Clears table at end.
    
    Inputs:
        table (Table): The Table with the player and dealer.
        round_num (int): The current round number
        player_bust (bool): True if player has gone bust; False otherwise
        player_natural (bool): True if player has a natural 21; False otherwise.
        
    Returns: None
    '''
    # check if player won
    if player_bust:
        print('Player went bust. Dealer wins round %d!\n' % round_num)
    elif player_natural:
        print('Player wins round %d with a NATURAL 21!\n' % round_num)
    
    # find who won after dealer's turn
    else:
        dealer_bust = table.dealerHit()
        if dealer_bust:
            print('Player wins round %d!\n' % round_num)
        else:
            table.whoWon()
            print('round %d!\n' % round_num)
        
    table.clearTable()


def play_again():
    '''
    Keeps asking player if they want to play again until valid entry provided.
    
    Inputs: N/A
    
    Returns: True if player wants to play again; False otherwise.
    '''
    # keep asking to play again until entry valid
    valid_entry = False
    while not valid_entry:
        play_again = input('Would you like to play another round (Y/N)? >> ')
        
        # check if entry valid and return bool
        if play_again[0].lower() == 'y':
            valid_entry = True
            return True
        elif play_again[0].lower() == 'n':
            valid_entry = True
            return False
        else:
            print('Invalid entry.', end=' ')
            

def goodbye_msg():
    ''' 
    Prints the goodbye message at the end of the game.
    
    Inputs: N/A
    
    Returns: None
    '''
    # print message
    print('\nThank you for playing. Goodbye...')

        
main()
