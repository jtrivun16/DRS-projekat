class User:
    def __init__(self, username: object, first_name: object, last_name: object, address: object, town: object, country: object, phone_number: object, email: object, cardNumber: object, verified: object, password: object) -> object:
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.town = town
        self.country = country
        self.phone_number = phone_number
        self.email = email
        self.cardNumber = cardNumber
        self.verified = verified
        self.password = password
  
        
        

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None