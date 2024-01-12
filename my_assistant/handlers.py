from classes import is_valid_birthday

from classes import is_valid_name

from classes import is_valid_email

from classes import is_valid_phone

from classes import Record

from classes import AddressBook

from classes import view_phone

from abc import ABC, abstractmethod


EXIT_MESSAGE = "Good bye!"

TEXT1 = ", next you can choose:"

TEXT2 = "contact, address, email, birthday, phone, note"

COMMAND_DESCRIPTIONS = {"a": ["add"+TEXT1, TEXT2],
                        "e": ["edit"+TEXT1, TEXT2],
                        "d": ["delete"+TEXT1, TEXT2],
                        "s": ["show"+TEXT1, "all contacts or all notes"],
                        "f": ["find, next you can choose: contact or note",""],
                        "u": ["show a list of upcoming birthdays",""],
                        "h": ["list of all commands",""],
                        "o": ["output of information: in a table or in strings", ""],
                        "q": ["exit the assistant", ""]}


class AllCommand(ABC):

    @abstractmethod
    def output(self):
        pass


class CommandToString(AllCommand):

    def output(self) -> None:
        print("\nAll commands:")
        for command, list_description in COMMAND_DESCRIPTIONS.items():
            print(f"    - {command}     - {list_description[0]}")
            if list_description[1]:
                    print(f"{' '*19}{list_description[1]}")
        print()


class CommandToTable(AllCommand):

    def output(self) -> None:
        max_len_description = 0
        for description in COMMAND_DESCRIPTIONS.values():
            len_description = len(description[0])
            if description[1]:
                len_description = len_description + 1 + len(description[1])
            if max_len_description < len_description:
                max_len_description = len_description
        max_len_description += 2
        divider = "-"*(max_len_description + 12)
        pattern = '|{:^9}|{:^'+str(max_len_description)+'}|'
        print(f"\n{' '*(max_len_description // 2)}All commands")
        print(divider)
        print(pattern.format("Command", "Description"))
        print(divider)
        for command, list_descriptions in COMMAND_DESCRIPTIONS.items():
            description = list_descriptions[0]
            if list_descriptions[1]:
                description = f"{description} {list_descriptions[1]}"
            print(pattern.format(command, description))
            print(divider)


def printn(text: str) -> None:
    print(f"\n{text}\n")

def print_all_commmands(book: AddressBook) -> None:
    if book.get_output_direction() == 's':
        commands = CommandToString()
    else:
        commands = CommandToTable()
    commands.output()

def choice_output() -> str:
    valid_output = ["t", "s"]
    prompt_text = "Select output of information: t - table or s - strings: "
    choice = ""
    while not choice in valid_output:
        choice = input(prompt_text).lower()
    return choice

def choice_of_two() -> str:
    valid_of_two = {"c": "contact", "n": "note"}
    prompt_text = "Select: c - contacts or n - notes: "
    choice = ""
    while not choice in valid_of_two:
        choice = input(prompt_text).lower()
    return valid_of_two[choice]

def choice_of_six() -> str:
    valid_of_six = {"c": "contact", "a": "address",
                    "e": "email", "b": "birthday",
                    "p": "phone", "n": "note"}
    prompt_text = "Select: c - contact, a - address, e - email,"\
                         " b - birthday, p - phone, n - note: "
    choice = ""
    while not choice in valid_of_six:
        choice = input(prompt_text).lower()
    return valid_of_six[choice]

def enter_the_name() -> str:
    name = input("Enter the name of the contact: ").strip()
    while not is_valid_name(name):
        name = input("Enter the valid name (more than two characters): ").strip()
    return name

def search_contact_by_name(book: AddressBook) -> Record:
    result = False
    name = input("Enter the name of the contact (e - exit): ").strip()
    while True:
        if name.lower() == "e":
            break
        if is_valid_name(name):
            if name in book.data:
                result = book.data[name]
                break
            else:
                print(f"Name {name} not found.")
        name = input("Enter the valid name (e - exit): ").strip()
    return result

def enter_the_birthday() -> str:
    birthday = input("Enter the birthday of the contact (e - exit): ").strip()
    while  not is_valid_birthday(birthday):
        if birthday.lower() == "e":
            birthday = ""
            break
        birthday = input("Enter the valid birthday (e - exit): ").strip()
    return birthday

def enter_the_address() -> str:
    address = input("Enter the address of the contact (e - exit): ").strip()
    if address.lower() == "e":
        address = ""
    return address

def enter_the_email() -> str:
    email = input("Enter the email of the contact (e - exit): ").strip()
    while not is_valid_email(email):
        if email.lower() == "e":
            email = ""
            break
        email = input("Enter the valid email (e - exit): ").strip()
    return email

def enter_the_phone() -> str:
    phone = input("Enter the phone of the contact (e - exit): ").strip()
    while not is_valid_phone(phone):
        if phone.lower() == "e":
            phone = ""
            break
        phone = input("Enter the valid phone (e - exit): ").strip()
    return phone

def enter_the_phones() -> list[str]:
    phones = []
    while True:
        phone = enter_the_phone()
        if phone:
            phones.append(phone)
        else:
            break
    return phones

def enter_the_note() -> str:
    note = input("Enter the note of the contact (e - exit): ").strip()
    if note.lower() == "e":
        note = ""
    return note

def enter_the_notes() -> list[str]:
    notes = []
    while True:
        note = enter_the_note()
        if note:
            notes.append(note)
        else:
            break            
    return notes

def enter_the_number_of_days(text: str) -> int:
    while True: 
        number_of_days = input(text)
        if number_of_days.isdigit():
            number_of_days = int(number_of_days)
            break
        else:
            print('Only numbers are required.')
    return number_of_days

def choice_of_phones(phones) -> int:
        text = "\n"
        for i in range(len(phones)):
            text = f"{text} {i + 1} - {view_phone(phones[i])}\n"
        text = f"{text}Select a number of the phone number: "
        while True:
            choice = input(text)
            if choice.isdigit():
                number = int(choice)
                if number > 0 and number < len(phones) + 1:
                    break
                else:
                    print('Incorrect number.')
            else:
                print('Only numbers are required.')
        return number - 1

def choice_of_notes(notes) -> int:
        text = "\n"
        for i in range(len(notes)):
            text = f"{text} {i + 1} - {notes[i]}\n"
        text = f"{text}Select a number of the note: "
        while True:
            choice = input(text)
            if choice.isdigit():
                number = int(choice)
                if number > 0 and number < len(notes) + 1:
                    break
                else:
                    print('Incorrect number.')
            else:
                print('Only numbers are required.')
        return number - 1

def choice_yes_no(text: str = "") -> str:
    choice = ""
    while choice != 'y' and choice != 'n':
        choice = input(f"{text} Yes - y or no - n: ").lower()
    return choice



def add_contact(book: AddressBook) -> None:
    name = enter_the_name()
    birthday = enter_the_birthday()
    address = enter_the_address()
    email = enter_the_email()
    phones = enter_the_phones()
    new_record = Record(name, birthday, address, email)
    for phone in phones:
        new_record.add_phone(phone)
    book.add_record(new_record)

def add_address(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        address = enter_the_address()
        record.add_address(address)

def add_email(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        email = enter_the_email()
        record.add_email(email)

def add_birthday(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        birthday = enter_the_birthday()
        record.add_birthday(birthday)

def add_phone(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        phones = enter_the_phones()
        for phone in phones:
            record.add_phone(phone)

def add_note(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        notes = enter_the_notes()
        for note in notes:
            record.add_note(note)


def add_handler(book: AddressBook) -> None:
    exec(f"add_{choice_of_six()}(book)")



def edit_contact(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        is_new_name = choice_yes_no("Shall we change the name of the contact?") == 'y'
        if is_new_name:
            book.delete(record.get_name())
            name = enter_the_name()
        birthday = enter_the_birthday()
        if birthday:
            record.add_birthday(birthday)
        address = enter_the_address()
        if address:
            record.add_address(address)
        email = enter_the_email()
        if email:
            record.add_email(email)
        phone = enter_the_phone()
        if phone:
            phones = record.list_phones()
            if len(phones) == 0:
                record.add_phone(phone)
            elif len(phones) == 1:
                record.edit_phone(phones[0], phone)
            else:
                record.edit_phone(phones[choice_of_phones(phones)], phone)
        if is_new_name:
            book.add_record(record)

def edit_address(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        address = enter_the_address()
        if address:
            record.add_address(address)

def edit_email(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        email = enter_the_email()
        if email:
            record.add_email(email)

def edit_birthday(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        birthday = enter_the_birthday()
        if birthday:
            record.add_birthday(birthday)

def edit_phone(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        phone = enter_the_phone()
        if phone:
            phones = record.list_phones()
            if len(phones) == 0:
                record.add_phone(phone)
            elif len(phones) == 1:
                record.edit_phone(phones[0], phone)
            else:
                record.edit_phone(phones[choice_of_phones(phones)], phone)

def edit_note(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        note = enter_the_note()
        if note:
            notes = record.list_notes()
            if len(notes) == 0:
                record.add_note(note)
            elif len(notes) == 1:
                record.edit_note(note)
            else:
                record.edit_note(notes[choice_of_notes(notes)], note)


def edit_handler(book: AddressBook) -> None:
    exec(f"edit_{choice_of_six()}(book)")



def del_contact(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        book.delete(record.get_name())

def del_address(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        record.del_address()

def del_email(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        record.del_email()

def del_birthday(book: AddressBook) -> None:
    record = search_contact_by_name(book)
    if record:
        record.del_birthday()

def del_phone(book: AddressBook) -> None:
    TEXT_TO_CONFIRM = "Confirm deletion of phone number"
    record = search_contact_by_name(book)
    if record:
        phones = record.list_phones()
        if len(phones) == 0:
            print("There are no phone numbers to delete.")
        elif len(phones) == 1:
            phone = view_phone(phones[0])
            if choice_yes_no(f"{TEXT_TO_CONFIRM} {phone}?") == 'y':
                record.del_phone(phones[0])
        else:
            choice = choice_of_phones(phones)
            phone = view_phone(phones[choice])
            if choice_yes_no(f"{TEXT_TO_CONFIRM} {phone}?") == 'y':
                record.del_phone(phones[choice])

def del_note(book: AddressBook) -> None:
    TEXT_TO_CONFIRM = "Confirm deletion of note"
    record = search_contact_by_name(book)
    if record:
        notes = record.list_notes()
        if len(notes) == 0:
            print("There are no notes to delete.")
        elif len(notes) == 1:
            if choice_yes_no(f"{TEXT_TO_CONFIRM} '{notes[0]}'?") == 'y':
                record.del_note(notes[0])
        else:
            choice = choice_of_notes(notes)
            if choice_yes_no(f"{TEXT_TO_CONFIRM} '{notes[choice]}'?") == 'y':
                record.del_note(notes[choice])


def del_handler(book: AddressBook) -> None:
    exec(f"del_{choice_of_six()}(book)")



def show_contact(book: AddressBook) -> None:
    text = book.find_by_string()
    if text:
        printn(text)
    else:
        printn("Contacts not found.")

def show_note(book: AddressBook) -> None:
    text = book.show_notes()
    if text:
        printn(text)
    else:
        printn("Notes not found.")


def show_handler(book: AddressBook) -> None:
    exec(f"show_{choice_of_two()}(book)")



def find_contact(book: AddressBook) -> None:
    context = input("Enter text to search: ")
    text = book.find_by_string(context)
    if text:
        printn(text)
    else:
        printn(f"Contacts with context '{context}' not found.")

def find_note(book: AddressBook) -> None:
    context = input("Enter text to search: ")
    text = book.show_notes(book.find_by_note(context))
    if text:
        printn(text)
    else:
        printn(f"Notes with context '{context}' not found.")


def find_handler(book: AddressBook) -> None:
    exec(f"find_{choice_of_two()}(book)")



def upcoming_birthdays_handler(book: AddressBook) -> None:
    number_of_days = enter_the_number_of_days("Enter the number of days"\
                                              " to check upcoming birthdays: ")
    text = book.upcoming_birthdays(number_of_days)
    if text:
        printn(text)
    else:
        printn(f"Contacts with birthdays in the next {number_of_days} "\
               "days not found.")


def set_output_handler(book: AddressBook) -> None:
    book.set_output(choice_output())


def quit_handler(book: AddressBook) -> bool:
    printn(EXIT_MESSAGE)
    return True


def invalid_command_handler(book: AddressBook) -> None:
    printn("The command was not found. Please enter valid command.")
