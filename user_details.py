class UserDetails:
    def __init__(
        self,
        email_id: str = None,
        role: str = None,
        experience: str = None,
        level:str = None,
        isExistingUser:bool = False,
        isSaved:bool = False,
        orders_list: [] = [],
        current_order: int = 0,
    ):
        self.email_id = email_id
        self.role = role
        self.experience = experience
        self.level = level
        self.isExistingUser = isExistingUser
        self.isSaved = isSaved
        self.orders_list = orders_list
        self.current_order = current_order