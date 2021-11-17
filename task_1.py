import datetime


class Customer:
    def __init__(self, name: str, card_details):
        self.name = name
        self.card_details = card_details
    
    def order_items(self, items, order_facade):
        try:
            print(order_facade.do_operation(items, self.card_details))
        except Exception as e:
            print(str(e))


class OrderFacade:
    def __init__(self, stock, shipment_provider):
        self.stock = stock
        self.shipment_provider = shipment_provider

    def do_operation(self, items, card_details):
        shopping_cart = ShoppingCart(self.stock)

        for item in items:
            shopping_cart.add_item(item, items[item])
        
        order = shopping_cart.checkout()
        shipment = Shipment(order, self.shipment_provider)

        order.payment.add_card_details(card_details)

        if order.payment.verify_payment():
            card_details['balance'] -= order.payment.amount
        else:
            raise Exception('Payment is not possible')
        
        return f'Order is successful\nTime of arrival: {shipment.time_of_arrival}\nTotal cost: {order.payment.amount}';


# Order Process Subsystem
class Order:
    def __init__(self, products):
        self.time = datetime.datetime.now()
        self.products = products

        cost = 0
        for product in self.products:
            cost += product.cost * self.products[product]

        self.payment = Payment(cost)

    def edit_order(self, products):
        self.time = datetime.datetime.now()
        self.products = products

        cost = 0
        for product in self.products:
            cost += product.cost * self.products[product]

        self.payment = Payment(cost)


class ShoppingCart:
    def __init__(self, stock):
        self.stock = stock
        self.items = {}

    def update_amount(self, item_description, amount_change):
        item = self.stock.select_stock_item(item_description, amount_change)
        if item not in self.items:
            self.items[item] = 0
        
        if self.items[item] + amount_change < 0:
            self.stock.select_stock_item(item_description, -amount_change)
            raise Exception(f'Not enough {item_description} in the shopping cart')
        
        self.items[item] += amount_change
    
    def add_item(self, item_description, amount):
        self.update_amount(item_description, amount)
    
    def checkout(self):
        return Order(self.items)


# Shipment Subsystem
class ShipmentProvider:
    def __init__(self, name: str, fee: float, transit_time: datetime.timedelta):
        self.name = name
        self.fee = fee
        self.transit_time = transit_time
    
    def modify_provider(self, name: str, fee: float, transit_time: datetime.timedelta):
        self.name = name
        self.fee = fee
        self.transit_time = transit_time


class Shipment:
    def __init__(self, order, provider: ShipmentProvider):
        self.order = order
        self.provider = provider
        self.time_of_arrival = order.time + provider.transit_time

        self.order.payment.amount += self.provider.fee
    
    def change_provider(self, new_provider: ShipmentProvider):
        self.time_of_arrival += -self.provider.transit_time + new_provider.transit_time
        self.order.payment.amount += -self.provider.fee + new_provider.fee
        self.provider = new_provider


# Inventory Sybsystem
class Product:
    def __init__(self, description: str, cost: float):
        self.description = description
        self.cost = cost
    
    def update_product(self, description: str, cost: float):
        self.description = description
        self.cost = cost


class Stock:
    def __init__(self):
        self.products = {}

    def update_stock(self, product: Product, amount_change: int):
        if product not in self.products:
            self.products[product] = 0
        
        if self.products[product] + amount_change < 0:
            raise Exception(f'Not enough {product.description} in stock')
        else:
            self.products[product] += amount_change
        
    def select_stock_item(self, item_description: str, amount: int):
        item = None
        for product in self.products:
            if product.description == item_description:
                item = product
                break

        if item is None:
            raise Exception(f'Not enough {item_description} in stock')
        
        self.update_stock(item, -amount)

        return item


# Payment Subsystem
class Payment:
    def __init__(self, amount: float):
        self.amount = amount
        self.card_details = None
    
    def add_card_details(self, card_details):
        self.card_details = card_details
    
    def verify_payment(self):
        if self.card_details == None:
            return False
        elif self.card_details['balance'] < self.amount:
            return False
        else: 
            return True


stock = Stock()
stock.update_stock(Product('Coca-Cola (2L)', 24.50), 20)
stock.update_stock(Product('Bread', 18.90), 5)
stock.update_stock(Product('Dutch Cheese', 41.20), 3)

shipment_provider = ShipmentProvider('SP-1', 175.00, datetime.timedelta(days=1, hours=8, minutes=30))
order_facade = OrderFacade(stock, shipment_provider)

customer = Customer('John Doe', { 'number': 1337, 'balance': 1703.58 })
items_to_order = {
    'Coca-Cola (2L)': 3,
    'Bread': 1,
    'Dutch Cheese': 1
}

print()
customer.order_items(items_to_order, order_facade)
print()