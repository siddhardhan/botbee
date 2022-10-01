class UserDetails:
    def __init__(
        self,
        email_id: str = None,
        role: str = None,
    ):
        self.email_id = email_id
        self.role = role
    
    def print(self):
        print("email ID:" + self.email_id)
        print("Role:" + self.role)