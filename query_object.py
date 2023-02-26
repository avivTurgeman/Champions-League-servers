from PL_player import PL_player


class query_obj:

    def __init__(self, query_name, is_exit=False) -> None:
        self.query_name = query_name
        self.EXIT = is_exit

    def do_query(self, data: list[PL_player]) -> list[PL_player]:
        ans = []
        if self.query_name == "full":
            return data
        if self.query_name == "Liverpool":
            for p in data:
                if p.get_team() == "Liverpool":
                    ans.insert(0, p)
        if self.query_name == "MCFC":
            for p in data:
                if p.get_team() == "MCFC":
                    ans.insert(0, p)
        if self.query_name == "Real Madrid":
            for p in data:
                if p.get_team() == "RMFC":
                    ans.insert(0, p)
        if self.query_name == "PSG":
            for p in data:
                if p.get_team() == "PSG":
                    ans.insert(0, p)
        if self.query_name == "Bayren Munich":
            for p in data:
                if p.get_team() == "FCBM":
                    ans.insert(0, p)
        if self.query_name == "Porto":
            for p in data:
                if p.get_team() == "Porto":
                    ans.insert(0, p)
        if self.query_name == "query21":
            pass
        if self.query_name == "query22":
            pass
        if self.query_name == "query23":
            pass
        if self.query_name == "query24":
            pass
        if self.query_name == "query25":
            pass
        if self.query_name == "query26":
            pass
        if self.query_name == "query31":
            pass
        if self.query_name == "query32":
            pass
        if self.query_name == "query33":
            pass
        if self.query_name == "query34":
            pass
        if self.query_name == "query35":
            pass
        if self.query_name == "query36":
            pass
        if self.query_name == "query41":
            for p in data:
                if p.get_age() > 25:
                    ans.insert(0, p)
        if self.query_name == "query42":
            for p in data:
                if p.get_age() < 28:
                    ans.insert(0, p)
        if self.query_name == "query43":
            pass
        if self.query_name == "query44":
            pass
        if self.query_name == "query45":
            pass
        if self.query_name == "query46":
            pass
        if self.query_name == "query51":
            pass
        if self.query_name == "query52":
            pass
        if self.query_name == "query53":
            pass
        if self.query_name == "query54":
            pass
        if self.query_name == "query55":
            pass
        if self.query_name == "query56":
            pass
        if self.query_name == "query61":
            pass
        if self.query_name == "query62":
            pass
        if self.query_name == "query63":
            pass
        if self.query_name == "query64":
            pass
        if self.query_name == "query65":
            pass
        return ans

    def is_exit(self):
        return self.EXIT
