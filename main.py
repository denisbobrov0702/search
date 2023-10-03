from collections import UserDict
from datetime import date,datetime
import pickle
import copy
import csv
import json

class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)
class Name(Field):
    
    def __init__(self, value):
        super().__init__(value)
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        if new_value.isalpha():
            self._value = new_value
        else:
            raise ValueError("It is not a name")
            

class Phone(Field):
    
    def __init__(self, value):
        
        super().__init__(value)
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Invalid phone number format")
        
        else:
            self._value=new_value
class Birthsday(Field):
    
    def __init__(self, value):
        
        super().__init__(value)
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        try:
            self._value = datetime.strptime(new_value, "%Y-%m-%d")
            
        except ValueError:
            print(f"Wrong format of date")
class Record:
    value=None
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found")
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    def days_to_birthday(self,birthday):
        current_date = date.today()
        if birthday:
            user_date=birthday.replace(year=current_date.year)
            delta_days=user_date-current_date
            if delta_days>=0:
                return delta_days
            else:
                user_date=birthday.replace(year=current_date.year+1)
                delta_days=user_date-current_date
                return delta_days

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    def iterator(self,N):
        self.N=N
        if self.N < len(self.data):
            
            return self.data[:N]
        raise StopIteration
    
    def save_address_book(self,filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.data, fh)
    def read_address_book_from_file(self,filename):
        with open(filename, "rb") as fh:
            unpacked = pickle.load(fh)
            return unpacked
    def search(self,query):
        users=[]
        for name,record in self.data.items():
            if query in name or any(query in i.value for i in record.phones):
                users.append(name)
            
        return users    
        