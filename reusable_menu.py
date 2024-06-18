import sys
import keyboard
import os
import time

class MenuTerminal:
    def __init__(self, items_menu, keys_functions) -> None:
        self.items_menu = items_menu
        self.keys_functions = keys_functions
        self.current_count = 0
    
    def event_keyboard(self):
        self.up_press = keyboard.on_press_key('up', lambda _: self.up())
        self.down_press = keyboard.on_press_key('down', lambda _: self.down())
    
    def down(self):
        self.current_count += 1  
        if self.current_count >= len(self.items_menu):
            self.current_count = 0
        self.display_menu()

    def up(self):
        self.current_count -= 1
        if self.current_count < 0:
            self.current_count = len(self.items_menu) - 1
        self.display_menu()
    
    def display_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for index, item in enumerate(self.items_menu):
            if index == self.current_count:
                print(f'> {item} <')
            else:
                print(item)

    def run(self):
        self.event_keyboard()
        self.display_menu()
        keyboard.wait('enter')
        self.execute_selection()

    def execute_selection(self):
        selected_function = self.keys_functions[self.current_count]
        selected_function()
        print(f'You selected: {selected_function}')

class MainMenu:
    def __init__(self, menu) -> None:
        self.menu = menu
        
    def get_menu(self) -> None:

        items_menu = list(self.menu.keys())
        keys_functions = list(self.menu.values())

        menu_terminal = MenuTerminal(items_menu, keys_functions)
        menu_terminal.run()


menu_ = {
    "Login" : "jes",
    "Create Account" : "Jes",
}

if __name__ == "__main__":

    menu = MainMenu(menu=menu_)
    menu.get_menu()










