class PL_player:
    def __init__(self, name: str, age: int, team: str, position: str, goals: int, assists: int) -> None:
        self.name = name
        self.age = age
        self.team = team
        self.position = position
        self.goals = goals
        self.assists = assists

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_team(self):
        return self.team

    def get_position(self):
        return self.position

    def get_goal(self):
        return self.goals

    def get_assists(self):
        return self.assists
