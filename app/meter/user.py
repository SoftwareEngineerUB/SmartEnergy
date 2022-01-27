from app.models.user import User

class UserObject:
    def __init__(self, user:User) -> None:
        self.user = user

    
    def getMonthlyStatistics(self, year, month):
        # TODO : Monthly consumption, most consuming device, mean daily consumption
        pass
        