
# import datetime
from datetime import datetime
from ab_classes_240723_w import AddressBook, Name, Phone, Record, Birthday
import re

address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NameError as e:
            print(
                f"Give me a name and phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except IndexError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except TypeError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except UnboundLocalError as e:
            print("Contact exists")
        except ValueError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except AttributeError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
    return wrapper


@input_error
def add_contact(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if len(args) == 2:
        pattern_bd = r'(\d\d)/(\d\d)/(\d{4})'
        if re.fullmatch(pattern_bd, args[1]):
            data = Birthday(args[1])
            if isinstance(data.value, datetime):
                birthday = data
                if rec:
                    # print(data)
                    birthday = data
                    return rec.add_birthday(birthday)
                rec = Record(name, birthday=birthday)
        else:
            pattern_ph = r"(\+\d{3}\(\d{2}\)\d{3}\-(?:(?:\d{2}\-\d{2})|(?:\d{1}\-\d{3}){1}))"
            if re.fullmatch(pattern_ph, args[1]):
                phone = Phone(args[1])
            if rec:
                return rec.add_phone(phone)
            rec = Record(name, phone=phone)

        return address_book.add_record(rec)
    if len(args) > 2:
        list_phones = []
        rec: Record = address_book.get(str(name))
        pattern_ph = r"(\+\d{3}\(\d{2}\)\d{3}\-(?:(?:\d{2}\-\d{2})|(?:\d{1}\-\d{3}){1}))"
        if rec:
            for i in range(1, len(args)):
                if re.fullmatch(pattern_ph, args[i]):
                    list_phones.append(Phone(args[i]))
                else:
                    continue
        else:
            for i in range(1, len(args)):
                if re.fullmatch(pattern_ph, args[i]):
                    list_phones.append(Phone(args[i]))
            rec = Record(name, list_phones)

        return address_book.add_record(rec)
    else:
        return "Unknown command"


# змінити
@input_error
def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


# Вийти
def exit_command(*args):
    return "Good bye!"


# показати контакт
@input_error
def get_phone(*args):
    name = Name(args[0])
    res: Record = address_book.get(str(name))
    result = res.get_phones(res)
    return f"{res.name} : {result}"


# Привіт
def hello(*args):
    return "How can I help you?"


# Невідома команда пуста команда
def no_command(*args, **kwargs):
    return "Unknown command"


# показати все
@input_error
def show_all_command(*args):
    if Record.__name__:
        return address_book
    return

# коли день народження


@input_error
def get_days_to_birthday(*args):
    name = Name(args[0])
    res: Record = address_book.get(str(name))
    result = res.days_to_birthday(res.birthday)
    if result == 0:
        return f'{name } tomorrow birthday'
    if result == 365:
        return f'{name} today is birthday'
    return f'{name} until the next birthday left {result} days'


# Видалити телефон
@input_error
def remove_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.remove_phone(phone)
    return f"No contact {name} in address book"

# Видалити запис


@input_error
def delete_record(*args):
    name = Name(args[0])
    if name.value in address_book:
        del address_book[name.value]
        return f"Contact '{name}' has been deleted from the address book."
    return f"No contact '{name}' found in the address book."


# Команди додати, змінити, видалити телефон, вихід, показати все, показати контакт
COMMANDS = {
    exit_command: ("good bye", "bye", "exit", "end", "close", "quit", "0"),
    add_contact: ("add ", "+ ", "1"),
    change_phone: ("change ", "зміни ", "2"),
    remove_phone: ("remove ", "delete ", "del ", "-", "3"),
    show_all_command: ("show all", "show", "4"),
    get_phone: ("phone ", "5"),
    get_days_to_birthday: ("birthday", "bd", "6"),
    delete_record: ("7"),
    hello: ("hello", "hi", "!",)
}


def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data
    return no_command, []


def main():
    while True:
        user_input = input(">>>")
        if user_input.startswith("pages"):
            rec_per_page = None
            try:
                rec_per_page = int(user_input[len("pages"):].strip())
            except ValueError:
                rec_per_page = 3
            for rec in address_book.iterator(rec_per_page):
                print(rec)
                input("For next page press any key")
        else:
            cmd, data = parser(user_input)
            result = cmd(*data)
            print(result)
            if cmd == exit_command:
                break


if __name__ == "__main__":
    main()
