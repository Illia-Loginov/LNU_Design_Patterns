import unittest
from task_2 import *


class TestTask2(unittest.TestCase):
    def setUp(self) -> None:
        self.bank = Bank(1, 'Skliana Banka', 'Lviv')
        self.teller = Teller(1, 'Tommy', self.bank)
        self.customer = Customer(1, 'Turkish', 'Lviv', '0451', self.bank)

        self.customer.open_account(self.teller, 1)
        self.customer.open_account(self.teller, 2)
        self.customer.apply_for_loan(self.teller, 1, 'Type 1', 3)
        self.customer.apply_for_loan(self.teller, 2, 'Type 2', 4)

    def test_copy(self) -> None:
        new_customer = copy.copy(self.customer)

        self.customer.id *= 10
        self.customer.bank.id *= 10
        for account_id in self.customer.accounts:
            self.customer.accounts[account_id].id *= 10
        for loan_id in self.customer.loans:
            self.customer.loans[loan_id].id *= 10

        self.assertNotEqual(self.customer.id, new_customer.id)
        self.assertEqual(self.customer.bank.id, new_customer.bank.id)

        self.assertEqual(self.customer.accounts[1].id, new_customer.accounts[1].id)
        self.assertEqual(self.customer.accounts[2].id, new_customer.accounts[2].id)

        self.assertEqual(self.customer.loans[1].id, new_customer.loans[1].id)
        self.assertEqual(self.customer.loans[2].id, new_customer.loans[2].id)

    def test_deepcopy(self) -> None:
        new_customer = copy.deepcopy(self.customer)

        self.customer.id *= 10
        self.customer.bank.id *= 10
        for account_id in self.customer.accounts:
            self.customer.accounts[account_id].id *= 10
        for loan_id in self.customer.loans:
            self.customer.loans[loan_id].id *= 10

        self.assertNotEqual(self.customer.id, new_customer.id)
        self.assertNotEqual(self.customer.bank.id, new_customer.bank.id)

        self.assertNotEqual(self.customer.accounts[1].id, new_customer.accounts[1].id)
        self.assertNotEqual(self.customer.accounts[2].id, new_customer.accounts[2].id)

        self.assertNotEqual(self.customer.loans[1].id, new_customer.loans[1].id)
        self.assertNotEqual(self.customer.loans[2].id, new_customer.loans[2].id)