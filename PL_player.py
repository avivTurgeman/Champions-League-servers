class PL_player:
    def __init__(self, name: str, rate: float, team: str, position: str, goals: int, assists: int) -> None:
        self.name = name
        self.rate = rate
        self.team = team
        self.position = position
        self.goals = goals
        self.assists = assists

    def get_name(self):
        return self.name

    def get_rate(self):
        return self.rate

    def get_team(self):
        return self.team

    def get_position(self):
        return self.position

    def get_goals(self):
        return self.goals

    def get_assists(self):
        return self.assists
