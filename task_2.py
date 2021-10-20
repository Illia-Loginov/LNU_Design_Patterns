import copy


class Account:
    def __init__(self, account_id: int, customer_id: int) -> None:
        self.id = account_id
        self.customer_id = customer_id


class Checking(Account):
    pass


class Savings(Account):
    pass


class Loan:
    def __init__(self, loan_id: int, type: str, account_id: int, customer_id: int):
        self.id = loan_id
        self.type = type
        self.account_id = account_id
        self.customer_id = customer_id


class Teller:
    def __init__(self, teller_id: int, name: str, bank):
        self.id = teller_id
        self.name = name
        self.bank = bank

    def collect_money():
        pass

    def open_account(self, customer, account_id: int):
        if account_id not in customer.accounts:
            customer.accounts[account_id] = Account(account_id, customer.id)

    def close_account(self, customer, account_id: int):
        if account_id in customer.accounts:
            del customer.accounts[account_id]

    def loan_request(self, customer, loan_id: int, loan_type: str, account_id: int):
        self.open_account(customer, account_id)
        if loan_id not in customer.loans:
            customer.loans[loan_id] = Loan(loan_id, loan_type, account_id, customer.id)

    def provide_info():
        pass

    def issue_card():
        pass


class Bank:
    def __init__(self, bank_id: int, name: str, location: str):
        self.id = bank_id
        self.name = name
        self.location = location
        
        self.tellers = []
        self.customers = []


class Customer:
    def __init__(self, customer_id: int, name: str, address: str, phone_number: int, bank: Bank):
        self.id = customer_id
        self.name = name
        self.address = address
        self.phone_number = phone_number

        self.bank = bank
        self.accounts = {}
        self.loans = {}

    def general_inquiry():
        pass

    def deposit_money():
        pass

    def withdraw_money():
        pass

    def open_account(self, teller: Teller, account_id: int):
        teller.open_account(self, account_id)

    def close_account(self, teller: Teller, account_id: int):
        teller.close_account(self, account_id)

    def apply_for_loan(self, teller: Teller, loan_id: int, loan_type: str, account_id: int):
        teller.loan_request(self, loan_id, loan_type, account_id)

    def request_card():
        pass

    def __copy__(self):
        customer = Customer(self.id, self.name, self.address, self.phone_number, self.bank)
        customer.accounts = self.accounts
        customer.loans = self.loans

        return customer

    def __deepcopy__(self, memo):
        customer = Customer(self.id, self.name, self.address, self.phone_number, copy.deepcopy(self.bank, memo))
        customer.accounts = copy.deepcopy(self.accounts, memo)
        customer.loans = copy.deepcopy(self.loans, memo)

        return customer