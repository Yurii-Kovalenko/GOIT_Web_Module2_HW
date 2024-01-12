from collections import UserDict

from datetime import datetime

from pathlib import Path

from json import load

from json import dump

from re import sub

from re import fullmatch

from re import IGNORECASE

from abc import ABC, abstractmethod


IS_DATE_GERMAN = True

IS_DATE_AMERICAN = not IS_DATE_GERMAN

if IS_DATE_GERMAN:
    DATE_TEMPLATE = "%d.%m.%Y"
    DATE_PROMPT = "DD.MM.YYYY"
else:
    DATE_TEMPLATE = "%m/%d/%Y"
    DATE_PROMPT = "MM/DD/YYYY"

NAME_FILE = Path(Path.home() / "contacts.json")

# Регулярний вираз для перевірки email
EMAIL_REGULAR = r"[a-z][a-z0-9_.]+[@][a-z.]+[.][a-z]{2,}"


def is_valid_birthday(birthday: str) -> bool:
    result = True
    if birthday:
        try:
            datetime.strptime(birthday, DATE_TEMPLATE)
        except:
            if birthday != 'e':
                print(f"Incorrect date {birthday}. Date in format {DATE_PROMPT} is required.")
            result = False    
    return result

def is_valid_name(name: str) -> bool:
    if len(name) < 3:
        print("The name must have more than 2 characters.")
        return False
    return True

def is_valid_email(email: str) -> bool:
    if fullmatch(EMAIL_REGULAR, email, flags = IGNORECASE):
        return True
    else:
        if email != 'e':
            print(f"Incorrect email {email}.")
    return False

def sanitazed(phone: str) -> str:
    return sub(r'\D', '', phone)
    
def is_valid_phone(phone: str) -> bool:
    if len(sanitazed(phone)) == 10:
        return True
    else:
        if phone != 'e':
            print(f"Incorrect phone number {phone}.")
    return False

def view_phone(phone: str) -> str:
    return f"({phone[:3]}){phone[3:6]}-{phone[6:8]}-{phone[8:]}"


class Record:
    def __init__(self, name: str, birthday: str = "",
                       address: str = "", email: str = ""):
        if is_valid_name(name):
            self.name = name
        else:
            raise ValueError
        if is_valid_birthday(birthday):
            self.birthday = birthday
        self.address = address
        self.email = email
        self.phones = []
        self.notes = []
    
    def edit_name(self, name: str) -> None:
        if is_valid_name(name):
            self.name = name

    def get_name(self) -> str:
        return self.name
    
    def add_birthday(self, birthday: str) -> None:
        if is_valid_birthday(birthday):
            self.birthday = birthday
    
    def del_birthday(self) -> None:
        self.birthday = ""
    
    def add_address(self, address: str) -> None:
        self.address = address
    
    def del_address(self) -> None:
        self.address = ""

    def add_email(self, email: str) -> None:
        if is_valid_email(email):
            self.email = email

    def del_email(self) -> None:
        self.email = ""

    def add_phone(self, phone: str) -> None:
        if is_valid_phone(phone) and not (sanitazed(phone) in self.phones):
            self.phones.append(sanitazed(phone))

    def del_phone(self, phone: str) -> None:
        if sanitazed(phone) in self.phones:
            self.phones.remove(sanitazed(phone))
        else:
            print(f"Phone number {phone} not found.")
    
    def edit_phone(self, phone_old: str, phone_new: str) -> None:
        if sanitazed(phone_old) in self.phones:
            if is_valid_phone(phone_new):
                index_phone = self.phones.index(sanitazed(phone_old))
                self.phones[index_phone] = sanitazed(phone_new)
        else:
            print(f"Phone number {phone_old} not found.")
    
    def list_phones(self) -> list[str]:
        return self.phones
    
    def add_note(self, note: str) -> None:
        if not note in self.notes:
            self.notes.append(note)

    def del_note(self, note: str) -> None:
        if note in self.notes:
            self.notes.remove(note)
        else:
            print(f"Note {note} not found.")
    
    def edit_note(self, old_note: str, new_note: str) -> None:
        if old_note in self.notes:
            self.notes[self.notes.index(old_note)] = new_note
        else:
            print(f"Note {old_note} not found.")
    
    def list_notes(self) -> list[str]:
        return self.notes
    
    def len_all_fields(self) -> list[int]:
        result = [0, 0, 0, 0, 0]
        result[0] = len(self.name)
        result[1] = len(self.birthday)
        result[2] = len(self.address)
        result[3] = len(self.email)
        len_phones = len(self.phones)
        result[4] = len_phones * 14
        if len_phones > 1:
            result[4] += (len_phones - 1) * 2
        return result
    
    def all_fields(self) -> list[str]:
        result = ["", "", "", "", ""]
        result[0] = self.name
        result[1] = self.birthday
        result[2] = self.address
        result[3] = self.email
        result[4] = '; '.join(view_phone(phone) for phone in self.phones)
        return result    
    
    def __str__(self) -> str:
        if self.birthday:
            birthday_text = f", birthday: {self.birthday}"
        else:
            birthday_text = ""
        if self.address:
            address_text = f", address: {self.address}"
        else:
            address_text = ""
        if self.email:
            email_text = f", email: {self.email}"
        else:
            email_text = ""
        if len(self.phones) > 0:
            s = ""
            if len(self.phones) > 1:
                s = "s"
            phones_text = '; '.join(view_phone(phone) for phone in self.phones)
            phones_text = f", phone{s}: {phones_text}"
        else:
            phones_text = ""
        return "Contact name: "\
               f"{self.name}{birthday_text}{address_text}"\
               f"{email_text}{phones_text}"



class ShowContacts(ABC):

    @abstractmethod
    def output(self):
        pass


class ShowContactsToStrings(ShowContacts):

    def output(self, records: list[Record]) -> str:
        result = []
        for record in records:
            result.append(str(record))
        return "\n".join(result)


class ShowContactsToTable(ShowContacts):

    def output(self, records: list[Record]) -> str:
        if not records:
            return ""
        result = []
        max_len_columns = [20, 10, 20, 20, 46]
        min_len_columns = 10
        len_coluns = [0, 0, 0, 0, 0]
        len_table = 16
        for record in records:
            len_record = record.len_all_fields()
            for i in range(len(len_coluns)):
                if len_coluns[i] < len_record[i]:
                    len_coluns[i] = len_record[i]
        for i in range(len(len_coluns)):
            if len_coluns[i] > max_len_columns[i]:
                len_coluns[i] = max_len_columns[i]
            if len_coluns[i] < min_len_columns:
                len_coluns[i] = min_len_columns
            len_table += len_coluns[i]
        
        divider = "-"*(len_table)
        pattern = '|'
        for i in range(len(len_coluns)):
            pattern += '{:^'+str(len_coluns[i]+2)+'}|'
        result.append(f"{' '*(len_table // 2 - 4)}Contacts")
        result.append(divider)
        result.append(pattern.format("Name", "Birthday", "Address", "Email", "Phones"))
        result.append(divider)
        for record in records:
            list_all_fields = record.all_fields()
            for i in range(len(len_coluns)):
                if len(list_all_fields[i]) > max_len_columns[i]:
                    list_all_fields[i] = list_all_fields[i][:max_len_columns[i]]
            
            result.append(pattern.format(list_all_fields[0], list_all_fields[1],
                                         list_all_fields[2], list_all_fields[3],
                                         list_all_fields[4]))
            result.append(divider)
        return "\n".join(result)


class ShowNotes(ABC):

    @abstractmethod
    def output(self):
        pass


class ShowNotesToStrings(ShowNotes):

    def output(self, notes: list) -> str:
        result = []
        for i in range(len(notes)):
            text_note  = f"N {str(i + 1)}, autor: {notes[i][0]}, note: {notes[i][1]}"
            result.append(text_note)
        return "\n".join(result)


class ShowNotesToTable(ShowNotes):

    def output(self, notes: list) -> str:
        result = []
        max_len_columns = [20, 70]
        min_len_columns = 10
        len_coluns = [0, 0]
        len_table = 17
        for note in notes:
            len_note = [len(note[0]), len(note[1])]
            for i in range(2):
                if len_coluns[i] < len_note[i]:
                    len_coluns[i] = len_note[i]
        for i in range(2):
            if len_coluns[i] > max_len_columns[i]:
                len_coluns[i] = max_len_columns[i]
            if len_coluns[i] < min_len_columns:
                len_coluns[i] = min_len_columns
            len_table += len_coluns[i]
        
        divider = "-"*(len_table)
        pattern = '|{:^10}|'
        for i in range(len(len_coluns)):
            pattern += '{:^'+str(len_coluns[i]+2)+'}|'
        result.append(f"{' '*(len_table // 2 - 3)}Notes")
        result.append(divider)
        result.append(pattern.format("N", "Autor", "Note"))
        result.append(divider)
        number = 0
        for note in notes:
            for i in range(2):
                if len(note[i]) > max_len_columns[i]:
                    note[i] = note[i][:max_len_columns[i]]
            result.append(pattern.format(str(number + 1), note[0], note[1]))
            result.append(divider)
            number += 1
        return "\n".join(result)


class AddressBook(UserDict):
    def __init__(self):
        self.data = dict()
        self.output_direction = "s"

    def set_output(self, output_direction: str) -> None:
        self.output_direction  = output_direction
    
    def get_output_direction(self) -> str:
        return self.output_direction
    
    def add_record(self, record: Record) -> None:
        self.data[record.name] = record

    def find_by_name(self, name_search: str) -> Record:
        for key in self.data:
            if key == name_search:
                return self.data[key]

    def delete(self, name_search: str) -> None:
        for key in self.data:
            if key == name_search:
                self.data.pop(key)
                break

    def find_by_string(self, string: str = "") -> str:
        records = []
        string = string.lower()
        for record in self.data.values():
            is_match = string in record.name.lower()
            is_match = is_match or (string in record.birthday.lower())
            is_match = is_match or (string in record.address.lower())
            is_match = is_match or (string in record.email.lower())
            for phone in record.phones:
                if is_match:
                    break
                is_match = is_match or (string in phone)
            if is_match:
                records.append(record)
        if records:
            return self.show_contacts(records)
        else:
            return ""
        
    def show_contacts(self, records: list[Record]) -> str:
        if self.output_direction == "s":
            output = ShowContactsToStrings()
        else:
            output = ShowContactsToTable()
        return output.output(records)
    
    def upcoming_birthdays(self, number_of_days: int) -> str:
        records = []
        today_date = datetime.today()
        today_date = datetime(today_date.year, today_date.month, today_date.day)
        for record in self.data.values():
            if record.birthday:
                date_of_birth : datetime = datetime.strptime(record.birthday,
                                                              DATE_TEMPLATE)
                next_birthday = datetime(today_date.year,
                                        date_of_birth.month, date_of_birth.day)
                if next_birthday < today_date:                                                                  
                    next_birthday = datetime(today_date.year + 1,
                                            date_of_birth.month, date_of_birth.day)
                delta = next_birthday - today_date
                # print(today_date, next_birthday, delta.days)
            if 0 <= delta.days <= number_of_days:                                                          
                records.append(record)
        if records:
            return self.show_contacts(records)
        else:
            return ""
    
    def find_by_note(self, string: str = "") -> list:
        result = []
        string = string.lower()
        for record in self.data.values():
            for note in record.notes:
                if string in note.lower():
                    result.append([record.get_name(), note, record])
        return result

    def show_notes(self, notes: list = []) -> str:
        if not notes:
            notes = self.find_by_note()
        if self.output_direction == "s":
            output = ShowNotesToStrings()
        else:
            output = ShowNotesToTable()
        return output.output(notes)
    
    def load_from_file(self) -> None:
        if not NAME_FILE.exists():
            return
        with open(NAME_FILE, "r") as fr:
            data_json = load(fr)
            records = data_json["contacts"]
            for record_json in records:
                new_record = Record(record_json["name"], record_json["birthday"],
                                    record_json["address"], record_json["email"])
                for phone in record_json["phones"]:
                    new_record.add_phone(phone)
                for note in record_json["notes"]:
                    new_record.add_note(note)
                self.add_record(new_record)

    def save_to_file(self) -> None:
        records = []
        for record in self.data.values():
            record_json = {"name": record.name,
                           "birthday": record.birthday,
                           "address": record.address,
                           "email": record.email,
                           "phones": [phone for phone in record.phones],
                           "notes": [note for note in record.notes]}
            records.append(record_json)
        with open(NAME_FILE, "w") as fw:
            dump({"contacts": records}, fw)
