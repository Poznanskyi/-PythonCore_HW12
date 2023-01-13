import pickle
from collections import UserDict
from datetime import datetime
from pathlib import Path


class Field:

    def __init__(self, value):
        self.value = value

    def __eq__(self, __o: object):
        if self.value == __o.value:
            return True
        return False

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):

    def sanitaze_phone_number(phone):

        try:
            new_phone = [str(int(i)) for i in new_phone]
        except ValueError:
            print("Number is not correct!")

        else:
            new_phone = "".join(new_phone)
            if len(new_phone) == 12:
                return f"+{new_phone}"
            elif len(new_phone) == 10:
                return f"+38{new_phone}"
            else:
                print("You number is wrong!")

        def __init__(self, value):
            self.value = Phone.sanitize_phone_number(value)

        @value.setter
        def value(self, value):
            self.value = Phone.sanitize_phone_number(value)

class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value:
            try:
                datetime.strptime(value, "%d.%m.%y")
            except ValueError:
                print("Data format must be 'DD.MM.YY")


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if isinstance(phone, Phone):
            self.phones.append(phone)

    def days_to_birthday(self):
        current_date = datetime.now().date()
        current_year = current_date.year

        if self.birthday:
            this_year_birthday = datetime(current_year, self.birthday.month, self.birthday.day).date()
            delta = this_year_birthday - current_date
            if delta.days >= 0:
                return f"Heppy Birthday {self.name} will be {delta.days} days!"
            else:
                next_year_birthday = datetime(current_year + 1, self.birthday.month, self.birthday.day).date()
                delta = next_year_birthday - current_date
                return f"Heppy Birthday {self.name} will be {delta.days} days!"

    def add_birthday(self, year, month, day):
        self.birthday = Birthday.validate_date(year, month, day)



    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def delete_phones(self):
        self.phones = []

    def delete_phone(self, phone: Phone):
        self.phones.remove[phone]

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.phones.remove(old_phone)
        self.phones.append(new_phone)

    def show_contact(self):
        return {"name": self.name, "phone": self.phones}



class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        if name in self.data:
            self.data.pop(name)

    def all_records(self):
        return {key: value.get_contact() for key, value in self.data.items()}

    def iterator(self):
        for record in self.data.values():
            yield record.get_contact()


    file_name = "AddressBook.bin"

    def readAB(file_name):
        with open(file_name, "rb") as file:
            unpacked = pickle.load(file)

    def writeAB(file_name):
        with open(file_name, "wb") as file:
            pickle.dump(file)


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)

    phone2 = Phone('129898989')
    rec.add_phone(phone2)
    assert len(ab['Bill'].phones) == 2
    old_phone = Phone('129898989')
    new_phone = Phone('9992345656')
    rec.change_phone(old_phone, new_phone)
    assert len(ab['Bill'].phones) == 2

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    print('All Ok)')
