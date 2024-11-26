
import os
from colorama import Fore, Style


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, default=None):
    response = input(prompt + Style.BRIGHT).strip()
    print(Style.RESET_ALL)
    return response if response else default or ""