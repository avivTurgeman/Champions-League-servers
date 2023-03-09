from PL_player import PL_player


def sort_answer(ans: list[PL_player], flag, reverse=True):
    if flag == "goals":
        return sorted(ans, key=lambda pl: pl.get_goals(), reverse=reverse)
    if flag == "assists":
        return sorted(ans, key=lambda pl: pl.get_assists(), reverse=reverse)
    if flag == "rating":
        return sorted(ans, key=lambda pl: pl.get_rate(), reverse=reverse)
    return ans


class query_obj:

    def __init__(self, query_name, is_exit=False) -> None:
        self.query_name = query_name
        self.EXIT = is_exit

    def do_query(self, data: list[PL_player]) -> list[PL_player]:
        flag = "none"
        ans: list[PL_player] = []
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
        if self.query_name == "no goals":
            flag = "rating"
            for p in data:
                if p.get_goals() == 0:
                    ans.insert(0, p)
        if self.query_name == "goals >= 2":
            flag = "goals"
            for p in data:
                if p.get_goals() >= 2:
                    ans.insert(0, p)
        if self.query_name == "goals < 4":
            flag = "goals"
            for p in data:
                if p.get_goals() < 4:
                    ans.insert(0, p)
        if self.query_name == "top scorer":
            max_score = -1
            top_scorer = None
            for p in data:
                if p.get_goals() >= max_score:
                    top_scorer = p
                    max_score = p.get_goals()
            ans.insert(0, top_scorer)
        if self.query_name == "top 10 scorers":
            flag = "goals"
            top_10 = []
            for i, p in enumerate(data):
                if i < 10:
                    top_10.insert(0, p)
                else:
                    for listed in top_10:
                        if p.get_goals() > listed.get_goals() or (
                                p.get_goals() == listed.get_goals() and p.get_assists() > listed.get_assists()):
                            top_10.remove(listed)
                            top_10.insert(0, p)
                            break

            ans = top_10
        if self.query_name == "top 5 scorers":
            flag = "goals"
            top_5 = []

            for counter, p in enumerate(data):
                if counter < 5:
                    top_5.insert(0, p)
                else:
                    for listed in top_5:
                        if p.get_goals() > listed.get_goals() or (
                                p.get_goals() == listed.get_goals() and p.get_assists() >= listed.get_assists()):
                            top_5.remove(listed)
                            top_5.insert(0, p)
                            break
            ans = top_5
        if self.query_name == "no assists":
            flag = "rating"
            for p in data:
                if p.get_assists() == 0:
                    ans.insert(0, p)
        if self.query_name == "assists >= 2":
            flag = "assists"
            for p in data:
                if p.get_assists() >= 2:
                    ans.insert(0, p)
        if self.query_name == "assists < 4":
            flag = "assists"
            for p in data:
                if p.get_assists() < 4:
                    ans.insert(0, p)
        if self.query_name == "top assistive":
            flag = "assists"
            max_score = -1
            top_assistive = None
            for p in data:
                if p.get_assists() >= max_score:
                    top_assistive = p
                    max_score = p.get_assists()
            ans.insert(0, top_assistive)
        if self.query_name == "top 10 assistive":
            top_10 = []
            for i, p in enumerate(data):
                if i < 10:
                    top_10.insert(0, p)
                else:
                    for listed in top_10:
                        if p.get_assists() > listed.get_assists() or (
                                p.get_assists() == listed.get_assists() and p.get_goals() > listed.get_goals()):
                            top_10.remove(listed)
                            top_10.insert(0, p)
                            break

            ans = top_10
        if self.query_name == "top 5 assistive":
            flag = "assists"
            top_5 = []
            for i, p in enumerate(data):
                if i < 5:
                    top_5.insert(0, p)
                else:
                    for listed in top_5:
                        if p.get_assists() > listed.get_assists() or (
                                p.get_assists() == listed.get_assists() and p.get_goals() > listed.get_goals()):
                            top_5.remove(listed)
                            top_5.insert(0, p)
                            break

            ans = top_5
        if self.query_name == "rating > 3.5":
            flag = "rating"
            for p in data:
                if p.get_rate() > 3.5:
                    ans.insert(0, p)
        if self.query_name == "rating < 7.0":
            flag = "rating"
            for p in data:
                if p.get_rate() < 7.0:
                    ans.insert(0, p)
        if self.query_name == "rating < 6.2":
            flag = "rating"
            for p in data:
                if p.get_rate() < 6.2:
                    ans.insert(0, p)
        if self.query_name == "rating > 7.5":
            flag = "rating"
            for p in data:
                if p.get_rate() > 7.5:
                    ans.insert(0, p)

        if self.query_name == "top 10 rating":
            flag = "rating"
            top_10 = []
            for i, p in enumerate(data):
                if i < 10:
                    top_10.insert(0, p)
                else:
                    for listed in top_10:
                        if p.get_rate() > listed.get_rate() or (
                                p.get_rate() == listed.get_rate() and p.get_goals() > listed.get_goals()):
                            top_10.remove(listed)
                            top_10.insert(0, p)
                            break

            ans = top_10
        if self.query_name == "top 5 rating":
            flag = "rating"
            top_5 = []
            for i, p in enumerate(data):
                if i < 5:
                    top_5.insert(0, p)
                else:
                    for listed in top_5:
                        if p.get_rate() > listed.get_rate() or (
                                p.get_rate() == listed.get_rate() and p.get_goals() > listed.get_goals()):
                            top_5.remove(listed)
                            top_5.insert(0, p)
                            break

            ans = top_5
        if self.query_name == "Goalkeepers":
            for p in data:
                if p.get_position() == "GK":
                    ans.insert(0, p)
        if self.query_name == "Defenders":
            for p in data:
                if p.get_position()[1] == "B":
                    ans.insert(0, p)
        if self.query_name == "midfielders":
            for p in data:
                if p.get_position()[1] == "M":
                    ans.insert(0, p)
        if self.query_name == "Forwards":
            for p in data:
                if p.get_position()[1] == "F":
                    ans.insert(0, p)
        if self.query_name == "Left Wing":
            for p in data:
                if p.get_position()[0] == "L":
                    ans.insert(0, p)
        if self.query_name == "Right Wing":
            for p in data:
                if p.get_position()[0] == "R":
                    ans.insert(0, p)

        ans = sort_answer(ans, flag)
        return ans

    def is_exit(self):
        return self.EXIT
