class PaymentCard:
    def __init__(self, number, name, expiry_date, security_code, user_id, balance):
        self.number = number
        self.user_name = name
        self.expiry_date = expiry_date
        self.security_code = security_code
        self.user_id = user_id
        self.balance = balance

        @staticmethod
        def payoff(amount, card_num):
            payment_card = PaymentCard.query.filter_by(card_number=card_num.data)
            if payment_card.balance >= amount:
                payment_card.balance -= amount
                return True

            # TODO else throw error

        @property
        def pay_in(self, amount, card_num):
            payment_card = PaymentCard.query.filter_by(card_number=card_num.data)

