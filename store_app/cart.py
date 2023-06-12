

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        self.items.append({
            'product': product,
            'quantity': quantity,
        })

    def remove_item(self, product):
        self.items = [item for item in self.items if item['product'] != product]

    def update_quantity(self, product, quantity):
        for item in self.items:
            if item['product'] == product:
                item['quantity'] = quantity
                break

    def get_total_quantity(self):
        total_quantity = sum(item['quantity'] for item in self.items)
        return total_quantity

    def get_total_price(self):
        total_price = sum(item['product'].price * item['quantity'] for item in self.items)
        return total_price

    def clear(self):
        self.items = []
