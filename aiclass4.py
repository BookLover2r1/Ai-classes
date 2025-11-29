import random
from colorama import init, Fore, Style
init(autoreset=True)

def display_board(board):
    print()
    def colored(cell):
        if cell == 'X':
            return Fore.RED + cell + Style.RESET_ALL
        elif cell == 'O':
            return Fore.BLUE + cell + Style.RESET_ALL
        else:
            return Fore.YELLOW + cell + Style.RESET_ALL 
    
    # Fixed: Proper print statements (removed + operators)
    print(' ' + colored(board[0]) + ' | ' + colored(board[1]) + ' | ' + colored(board[2]))
    print('-----------')
    print(' ' + colored(board[3]) + ' | ' + colored(board[4]) + ' | ' + colored(board[5]))
    print('-----------')
    print(' ' + colored(board[6]) + ' | ' + colored(board[7]) + ' | ' + colored(board[8]))
    print()

def player_choice():
    symbol = ''
    while symbol not in ['X','O']:
        symbol = input(Fore.GREEN + 'Choose X or O: ' + Style.RESET_ALL).upper()
    if symbol == 'X':
        return 'X', 'O'  # Fixed: Return tuple properly
    else:
        return 'O', 'X'

def player_move(board, symbol):
    while True:
        try:
            move = int(input(Fore.CYAN + "Enter your move (1-9): " + Style.RESET_ALL))
            if move in range(1, 10) and board[move - 1].isdigit():
                board[move - 1] = symbol
                return
            else:
                print(Fore.RED + "Invalid move! Choose empty number (1-9)." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Please enter a number between 1-9!" + Style.RESET_ALL)

def ai_move(board, ai_symbol, player_symbol):
    # Check for AI win
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = ai_symbol
            if check_win(board_copy, ai_symbol):
                board[i] = ai_symbol
                return
    
    # Block player win
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = player_symbol
            if check_win(board_copy, player_symbol):
                board[i] = ai_symbol
                return
    
    # Random move if no win/block
    possible_moves = [i for i in range(9) if board[i].isdigit()]
    move = random.choice(possible_moves)
    board[move] = ai_symbol

def check_win(board, symbol):
    win_conditions = [
        (0,1,2), (3,4,5), (6,7,8),  # Rows
        (0,3,6), (1,4,7), (2,5,8),  # Columns
        (0,4,8), (2,4,6)            # Diagonals
    ]
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] == symbol:
            return True
    return False

def check_full(board):
    return all(not spot.isdigit() for spot in board)

def tic_tac_toe():
    print(Fore.MAGENTA + '🎮 Welcome to Tic Tac Toe! 😀' + Style.RESET_ALL)
    player_name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL)
    
    while True:
        board = ['1','2','3','4','5','6','7','8','9']
        player_symbol, ai_symbol = player_choice()
        
        # Player goes first if X, AI first if player chose O
        current_player = 'Player' if player_symbol == 'X' else 'AI'
        
        print(Fore.YELLOW + f"\n{player_name} ({player_symbol}) vs AI ({ai_symbol})" + Style.RESET_ALL)
        input(Fore.CYAN + "Press Enter to start..." + Style.RESET_ALL)
        
        game_on = True
        while game_on:
            display_board(board)
            
            if current_player == 'Player':
                player_move(board, player_symbol)
            else:
                print(Fore.BLUE + "🤖 AI is thinking..." + Style.RESET_ALL)
                ai_move(board, ai_symbol, player_symbol)
            
            # Check win after move
            if check_win(board, player_symbol):
                display_board(board)
                print(Fore.GREEN + f"🎉 {player_name} WINS!" + Style.RESET_ALL)
                break
            elif check_win(board, ai_symbol):
                display_board(board)
                print(Fore.RED + "🤖 AI WINS! Better luck next time!" + Style.RESET_ALL)
                break
            elif check_full(board):
                display_board(board)
                print(Fore.YELLOW + "🤝 It's a TIE!" + Style.RESET_ALL)
                break
            
            # Switch turns
            current_player = 'AI' if current_player == 'Player' else 'Player'
        
        # Play again?
        play_again = input(Fore.GREEN + "\nPlay again? (y/n): " + Style.RESET_ALL).lower()
        if play_again != 'y':
            print(Fore.MAGENTA + "Thanks for playing! 👋" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    tic_tac_toe()
r