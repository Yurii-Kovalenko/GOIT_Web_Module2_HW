from os import path as ospath
 
from sys import path

path.append(ospath.dirname(ospath.realpath(__file__)))

from classes import AddressBook

from handlers import print_all_commmands

from handlers import invalid_command_handler

from handlers import add_handler

from handlers import edit_handler

from handlers import del_handler

from handlers import show_handler

from handlers import find_handler

from handlers import upcoming_birthdays_handler

from handlers import quit_handler

from handlers import set_output_handler

PROMPT_TEXT = 'Write a command ( h (help) - all commands): '

EXIT_COMMANDS = ["q", "close", "exit", "quit"]

COMMAND_HANDLERS = {"a": add_handler,
                    "e": edit_handler,
                    "d": del_handler,
                    "s": show_handler,
                    "f": find_handler,
                    "u": upcoming_birthdays_handler,
                    "h": print_all_commmands,
                    "help": print_all_commmands,
                    "o": set_output_handler
                    }

for exit_command in EXIT_COMMANDS:
    COMMAND_HANDLERS[exit_command] = quit_handler

def main() -> None:

    my_book = AddressBook()
    my_book.load_from_file()

    print("Hi! I am your assistant. How can I help you?")
    command = input(PROMPT_TEXT).lower()
    is_exit = False

    while not is_exit:
        is_exit = COMMAND_HANDLERS.get(command,
                                        invalid_command_handler)(my_book)
        if not is_exit:
            command = input(PROMPT_TEXT).lower()
    
    my_book.save_to_file()
    

if __name__ == "__main__":
    main()