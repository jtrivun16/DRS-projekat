class OnlinePaymentCard:
    def __init__(self, number, name, expiry_date, security_code, status):
        self.number = number
        self.user_name = name
        self.expiry_date = expiry_date
        self.security_code = security_code
        self.status = status