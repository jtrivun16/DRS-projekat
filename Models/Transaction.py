class Transaction:
    def __init__(self, id, sender, receiver, amount, date, currency, state, rsd_equivalent) -> None:
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.date = date
        self.currency = currency
        self.state = state
        self.rsd_equivalent = rsd_equivalent  # TODO bolji naziv

