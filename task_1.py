from dataclasses import dataclass
import random
import hashlib


class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: str) -> None:
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self.hashed_cvv = self.hash(cvv)

    @property
    def hashed_cvv(self):
        return self._hashed_cvv
    
    @hashed_cvv.setter
    def hashed_cvv(self, value):
        self._hashed_cvv = value

    def give_details(self, *args):
        return {
            'client': self.client,
            'account_number': self.account_number,
            'credit_limit': self.credit_limit,
            'grace_period': self.grace_period,
            'hashed_cvv': self.hashed_cvv,
        }

    @staticmethod
    def create_number(digits: int) -> str:
        result = ''
        for i in range(digits):
            result += str(random.randint(0, 9))
        
        return result

    def hash(self, value: str) -> str:
        return hashlib.sha256(bytes(value, 'UTF-8')).hexdigest()
    
    def verify_cvv(self, value: str) -> str:
        return (self.hash(value) == self._hashed_cvv)


class BankInfo:
    def __init__(self, bank_name: str, holder_name: str):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.account_numbers = {}
        self.credit_history = {}

    def transaction_list(self, account_number: str):
        if account_number in self.credit_history:
            return self.credit_history[account_number]['transaction_list']
        else:
            return []


@dataclass
class PersonalInfo:
    id: int
    first_name: str
    last_name: str
    address: str
    phone_number: str
    email: str


class BankCustomer:
    default_credit_limit = 500
    default_grace_period = 10

    def __init__(self, personal_info: PersonalInfo, bank_details: BankInfo):
        self._personal_info = personal_info
        self.bank_details = bank_details

    @property
    def personal_info(self):
        return self._personal_info

    @personal_info.setter
    def personal_info(self, value):
        self._personal_info = value

    def create_credit_card(self) -> str:
        client = f'{self._personal_info.first_name} {self._personal_info.last_name}'
        account_number = CreditCard.create_number(16)
        cvv = CreditCard.create_number(4)
        
        credit_card = CreditCard(client, account_number, self.default_credit_limit, self.default_grace_period, cvv)
        
        self.bank_details.account_numbers[client] = {
            'account_number': credit_card.account_number,
            'hashed_cvv': credit_card.hashed_cvv
        }

        self.bank_details.credit_history[account_number] = {
            'transaction_list': [],
            'credit_limit': self.default_credit_limit,
            'grace_period': self.default_grace_period
        }

        return cvv

    @property
    def credit_card(self) -> CreditCard:
        client = f'{self._personal_info.first_name} {self._personal_info.last_name}'

        if client not in self.bank_details.account_numbers:
            return None

        account_number = self.bank_details.account_numbers[client]['account_number']
        credit_limit = self.bank_details.credit_history[account_number]['credit_limit']
        grace_period = self.bank_details.credit_history[account_number]['grace_period']
        hashed_cvv = self.bank_details.account_numbers[client]['hashed_cvv']

        credit_card = CreditCard(client, account_number, credit_limit, grace_period, '0000')
        credit_card.hashed_cvv = hashed_cvv

        return credit_card


    def give_bank_details(self, *args):
        client = f'{self._personal_info.first_name} {self._personal_info.last_name}'
        credit_card = self.credit_card
        account_number = None if credit_card is None else credit_card.account_number

        return {
            'bank_name': self.bank_details.bank_name,
            'client': client,
            'account_number': account_number,
            'transaction_list': self.bank_details.transaction_list(account_number)
        }


class BankCustomerDecorator(BankCustomer):
    default_credit_limit = BankCustomer.default_credit_limit
    default_grace_period = BankCustomer.default_grace_period
    
    def __init__(self, bank_customer) -> None:
        if isinstance(bank_customer, BankCustomerDecorator):
            self._bank_customer = bank_customer.bank_customer
        else:
            self._bank_customer = bank_customer

        self._bank_customer.default_credit_limit = self.default_credit_limit
        self._bank_customer.default_grace_period = self.default_grace_period

        credit_card = self._bank_customer.credit_card
        if credit_card is not None:
            self._bank_customer.bank_details.credit_history[credit_card.account_number]['credit_limit'] = self.default_credit_limit
            self._bank_customer.bank_details.credit_history[credit_card.account_number]['grace_period'] = self.default_grace_period
    
    @property
    def bank_customer(self):
        return self._bank_customer

    @property
    def personal_info(self):
        return self._bank_customer.personal_info

    @personal_info.setter
    def personal_info(self, value):
        self._bank_customer.personal_info = value

    def create_credit_card(self) -> CreditCard:
        return self._bank_customer.create_credit_card()

    @property
    def credit_card(self) -> CreditCard:
        return self._bank_customer.credit_card

    def give_bank_details(self, *args):
        return self._bank_customer.give_bank_details(*args)


class IndividualCustomer(BankCustomerDecorator):
    default_credit_limit = 5000
    default_grace_period = 20

    def __init__(self, bank_customer: BankCustomer) -> None:
        super().__init__(bank_customer)


class CorporateCustomer(BankCustomerDecorator):
    default_credit_limit = 25000
    default_grace_period = 60

    def __init__(self, bank_customer: BankCustomer) -> None:
        super().__init__(bank_customer)


class VIPCustomer(BankCustomerDecorator):
    default_credit_limit = 100000
    default_grace_period = 120

    def __init__(self, bank_customer: BankCustomer) -> None:
        super().__init__(bank_customer)


bank = BankInfo('Bank 1', 'John Doe')
customer = BankCustomer(PersonalInfo(1, 'Kyle', 'Carpenter', '18 Ilchester Road', '077 7060 1603', 'KyleCarpenter@teleworm.us'), bank)

print('\n### BANK DETAILS ###')

print('\n\tBank details before card creation:')
print(customer.give_bank_details())

cvv = customer.create_credit_card()

print('\n\tBank details after card creation:')
print(customer.give_bank_details())

print('\n### CARD DETAILS ###')
print(f'CVV: {cvv}')
print(f'CVV verification result: {customer.credit_card.verify_cvv(cvv)}')

print('\n\tDefault customer:')
print(customer.credit_card.give_details())

customer = IndividualCustomer(customer)
print('\n\tIndividual customer:')
print(customer.credit_card.give_details())

customer = CorporateCustomer(customer)
print('\n\tCorporate customer:')
print(customer.credit_card.give_details())

customer = VIPCustomer(customer)
print('\n\tVIP customer:')
print(customer.credit_card.give_details())
