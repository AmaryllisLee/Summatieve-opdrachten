class Team:
  
    def __init__(self,name, average_home_score, average_home_conceded,average_away_score ,average_away_conceded, prob_list_teams):
        self.name = name
        self.ahs = average_home_score
        self.ahc = average_home_conceded
        self.aas = average_away_score
        self.aac = average_away_conceded
        self.prob_list_teams = prob_list_teams
        
        
        self.score = 0 # houd de score bij van de team
        self.doelsaldo = 0 # houd de doelsaldo bij van de team
    