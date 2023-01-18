class Transaction:
    def __init__(self, transaction_number, sender, receiver, amount, date, state):
        self.transaction_number = transaction_number
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.date = date
        self.state = state


