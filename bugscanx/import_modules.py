
import os
from colorama import Fore, Style


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, default=None, min_value=None, max_value=None, validator=None, error_message="Invalid input, please try again."):
    """
    Enhanced utility function to get user input with validation support.

    Parameters:
    - prompt (str): The message to display to the user.
    - default (str, optional): Default value if the user does not provide input.
    - validator (function, optional): A function to validate the input. 
      It should return True if valid, otherwise False.
    - error_message (str, optional): Message to display for invalid inputs.

    Returns:
    - str: The validated user input or the default value.
    """
    while True:
        try:
            # Add the default value to the prompt if available
            full_prompt = f"{prompt} [{default}] " if default else f"{prompt} "
            response = input(full_prompt + Style.BRIGHT).strip()
            print(Style.RESET_ALL)  # Reset styles after user input
            
            # Use the default value if no input is provided
            if not response and default is not None:
                return default
            
            # Validate the input if a validator is provided
            if validator:
                if validator(response, min_value, max_value):
                    return response
                else:
                    print(error_message)
            else:
                return response
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")  # Handle Ctrl+C or Ctrl+D gracefully
            exit(0)


def validate_input_range(value, min_value, max_value):
    """
    Validator function to check if the input is an integer within a specified range.

    Parameters:
    - value (str): The user input as a string.
    - min_value (int): The minimum valid value (default is 0).
    - max_value (int): The maximum valid value (default is 11).

    Returns:
    - bool: True if the input is a valid integer within the specified range, otherwise False.
    """
    if value.isdigit():
        num = int(value)
        return min_value <= num <= max_value
    return False