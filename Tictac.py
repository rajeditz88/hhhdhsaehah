from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import random


class TicTacToeApp(App):
    def build(self):
        self.game = TicTacToeGame()
        return self.game


class TicTacToeGame(BoxLayout):
    def __init__(self, **kwargs):
        super(TicTacToeGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.start_menu()

    def start_menu(self):
        self.clear_widgets()

        title = Label(text='Tic Tac Toe', font_size=80, bold=True, color=(0, 0, 0, 1))  # Black title color
        self.add_widget(title)

        start_button = Button(text="Start Game", font_size=30, on_press=self.start_game_menu, background_color=(1, 1, 1, 1))
        exit_button = Button(text="Exit Game", font_size=30, on_press=self.stop, background_color=(0.8, 0.8, 0.8, 1))

        self.add_widget(start_button)
        self.add_widget(exit_button)

    def start_game_menu(self, instance):
        self.clear_widgets()

        title = Label(text="Choose Opponent", font_size=50, bold=True, color=(0, 0, 0, 1))
        self.add_widget(title)

        ai_button = Button(text="Play with AI", font_size=30, on_press=self.play_with_ai, background_color=(1, 1, 1, 1))
        human_button = Button(text="Play with Human", font_size=30, on_press=self.play_with_human, background_color=(0.9, 0.9, 0.9, 1))
        back_button = Button(text="Back to Menu", font_size=30, on_press=self.start_menu, background_color=(0.8, 0.8, 0.8, 1))

        self.add_widget(ai_button)
        self.add_widget(human_button)
        self.add_widget(back_button)

    def play_with_ai(self, instance):
        self.clear_widgets()
        self.game_board = TicTacToeBoard(is_ai_game=True)
        self.add_widget(self.game_board)

    def play_with_human(self, instance):
        self.clear_widgets()
        self.game_board = TicTacToeBoard(is_ai_game=False)
        self.add_widget(self.game_board)

    def stop(self, instance):
        App.get_running_app().stop()


class TicTacToeBoard(BoxLayout):
    def __init__(self, is_ai_game, **kwargs):
        super(TicTacToeBoard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.is_ai_game = is_ai_game
        self.cols = 3
        self.board = [None, None, None, None, None, None, None, None, None]  # The game grid
        self.player_turn = True  # Player starts
        self.ai_turn = False  # AI starts after player
        self.winner = None
        self.buttons = []
        self.create_board()

    def create_board(self):
        grid = GridLayout(cols=3)  # Ensure a 3x3 grid layout
        for i in range(9):
            btn = Button(font_size=120, bold=True, on_press=self.make_move, background_normal='', background_color=(1, 1, 1, 1))  # White background
            btn.index = i
            self.buttons.append(btn)
            grid.add_widget(btn)
        self.add_widget(grid)

    def make_move(self, btn):
        if self.board[btn.index] is None and self.winner is None:
            self.board[btn.index] = 'X' if self.player_turn else 'O'
            btn.text = 'X' if self.player_turn else 'O'
            btn.color = (0, 0, 0, 1)  # Black color for "X" and "O" text
            btn.font_size = 120  # Larger font size
            self.check_winner()
            self.switch_turn()
            if self.is_ai_game and not self.player_turn:  # AI move after player
                self.ai_move()
                self.check_winner()

    def switch_turn(self):
        self.player_turn = not self.player_turn
        self.ai_turn = not self.ai_turn

    def ai_move(self):
        if self.ai_turn and self.winner is None:
            empty_spots = [i for i, x in enumerate(self.board) if x is None]
            move = random.choice(empty_spots)
            self.board[move] = 'O'
            self.buttons[move].text = 'O'
            self.buttons[move].color = (0, 0, 0, 1)  # Black for AI "O"
            self.switch_turn()

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != None:
                self.winner = self.board[combo[0]]
                self.show_winner_popup(self.winner)
                return

        if None not in self.board:
            self.show_winner_popup('Draw')

    def show_winner_popup(self, winner):
        for btn in self.buttons:
            btn.disabled = True

        # Create the winner popup with an option to play again
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f'{winner} Wins!', font_size=40, color=(0, 0, 0, 1)))  # Black for win text
        
        play_again_button = Button(text="Play Again", on_press=self.play_again, background_color=(1, 1, 1, 1), font_size=30)
        exit_button = Button(text="Exit Game", on_press=self.stop, background_color=(0.8, 0.8, 0.8, 1), font_size=30)
        
        content.add_widget(play_again_button)
        content.add_widget(exit_button)

        popup = Popup(title='Game Over', content=content, size_hint=(0.5, 0.5))
        popup.open()

    def play_again(self, instance):
        self.clear_widgets()
        self.board = [None, None, None, None, None, None, None, None, None]
        self.winner = None
        self.create_board()
        self.player_turn = True
        self.ai_turn = False

    def stop(self, instance):
        App.get_running_app().stop()


if __name__ == '__main__':
    TicTacToeApp().run()
