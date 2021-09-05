class Payment:
    def __init__(self, amount):
        self.amount = amount


class Cash(Payment):
    def __init__(self, amount, currency):
        super().__init__(amount)
        self.currency = currency


class Check(Payment):
    def __init__(self, amount, name, bank_id):
        super().__init__(amount)
        self.name = name
        self.bank_id = bank_id

    def authorized(self):
        return True


class Credit(Payment):
    def __init__(self, amount, number, credit_type, expiration_date):
        super().__init__(amount)
        self.number = number
        self.type = credit_type
        self.expiration_date = expiration_date

    def authorized(self):
        return True


class Item:
    def __init__(self, weight, description):
        self.weight = weight
        self.description = description

    def get_tax(self):
        return (self.weight / 200) * 0.4

    def get_price(self):
        return self.weight * 60


class OrderDetail:
    def __init__(self, quantity, tax_status):
        self.quantity = quantity
        self.tax_status = tax_status


class Order:
    def __init__(self, date, status, quantity, tax_status, item):
        self.date = date
        self.status = status
        self.order_detail = OrderDetail(quantity, tax_status)
        self.item = item

    def calc_tax(self):
        return Payment(self.item.get_tax() * self.item.get_price() * self.order_detail.quantity)

    def calc_total(self):
        return Payment((self.item.get_tax() + 1) * self.item.get_price() * self.order_detail.quantity)


class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.orders = []
