import math
class Tournament:
    """
    Een class waar zo'n tournament plaatvind tussen gegeven spelers.

    In deze class wordne twee soorten wedstrijd:
    1. wedstrijden_prob_list - Implementatie van de normale opdracht
        In deze implementatie wordt een competitie gespeeld met de gegeven tabel vabn kansen.

    2. wedstrijden_verdiepend - Implementatie van de verdiepende opdracht.
        In deze implementatie wordt er rekening gehouden met de doelsaldo. 
        Er wordt een betere, granuleerder beeld te schetsen van de waarschijnlijk uitkomst van een competitie dmv Poisson verdeling. 

    Er wordt ervoor gekozen om beide soorten te gebruiken, om de resultaten te vergelijken.
    
    Disclaimer: Er wordt gebruikt van engelse woorden die naar  bepaalde termen uit de opdracht verwijst.

    """
    
    def __init__(self, rng):
        self.teams = []
        self.rng = rng
        
    def gemiddelde_thuis_scoort(self):
        'Bereken de totale average home score van alle teams'
        sum_ahs = 0
        for team in self.teams:
            sum_ahs += team.ahs
        
        return sum_ahs/len(self.teams)
    
    def gemiddelde_thuis_toegegeven(self):
        'Bereken de totale average home conceded van alle teams'
        sum_ahc = 0
        for team in self.teams:
            sum_ahc += team.ahc
        
        return sum_ahc/len(self.teams)
    
    def gemiddelde_uit_scoort(self):
        'Bereken de totale average away score van alle teams'
        sum_aas = 0
        for team in self.teams:
            sum_aas += team.aas
        
        return sum_aas/len(self.teams)
    
    def gemiddelde_uit_toegegeven(self):
        'Bereken de totale average away conceded van alle teams'
        sum_aac = 0
        for team in self.teams:
            sum_aac += team.aac
        
        return sum_aac/len(self.teams)
    
    def thuis_aanvalskracht(self, thuisploeg): 
        'Berekenen van Attack Strength van de thuisploeg/hometeam'
        return thuisploeg.ahs/ self.gemiddelde_thuis_scoort()
    
    def uit_aanvalskracht(self, tegenstander): 
        'Berekenen van Attack Strength van de tegenstander/awayteam'
        return tegenstander.aas/ self.gemiddelde_uit_scoort()
    
    def thuis_verdedigingskracht(self, thuisploeg): # 'Defense Strength'
        'Berekenen van Defense Strength Strength van de thuisploeg/hometeam'
        return thuisploeg.ahc/ self.gemiddelde_thuis_toegegeven()
    
    def uit_verdedigingskracht(self, tegenstander): # 'Defense Strength'
        'Berekenen van Defense Strength Strength van de tegenstander/awayteam'
        return tegenstander.aac/ self.gemiddelde_uit_toegegeven()
    
    def thuis_doelpunten(self, thuisploeg, tegenstander):
        'Berekenen van de doelpunten voor de thuisploeg'
        return self.thuis_aanvalskracht(thuisploeg) * self.uit_verdedigingskracht(tegenstander) * self.gemiddelde_thuis_scoort()
    
    def uit_doelpunten(self, thuisploeg, tegenstander):
        'Berekenen van de doelpuntne voor de tegenstander'
        return self.uit_aanvalskracht(tegenstander) * self.thuis_verdedigingskracht(thuisploeg) * self.gemiddelde_uit_scoort()
        
    def poisson_verdeling(self, expected_occurences, discrete_events):
        'Functie die de Poissson verdeling implementeert'
        return math.e**(-expected_occurences) * ((expected_occurences**discrete_events)/math.factorial(discrete_events))
    
    
    def match_outcome(self,thuisploeg, tegenstander):
        'Bepaal de doelpunten voor de thuisploeg en de tegenstander dmv Poisson verdeling'
        random_number = self.rng.randdec() # pakt random getal
        kans_doelpunten_verdeling = 0
        r = 20
        #Bepaal de kans voor  0-0, 0-1, 1-0, 1-1, ... r-r
        for x in range(r+1):
            for y in range(r+1):
                thuis_kans_doelpunt = self.poisson_verdeling(self.thuis_doelpunten(thuisploeg, tegenstander), x) # pakt de kans dat thuisploeg x doelpunten scoort
                uit_kans_doelpunt   = self.poisson_verdeling(self.uit_doelpunten(thuisploeg, tegenstander), y) # pakt de kans dat tegenstander y doelpunten scoort.
                
                kans_doelpunten_verdeling += thuis_kans_doelpunt * uit_kans_doelpunt 
                
                if random_number <= kans_doelpunten_verdeling:
                    return x, y
        return r, r # return gelijk punten (r, r) als rng is groter dan de kans voor r-r. Hiermee wordt voorkomen dat de functie crasht.

                
    def wedstrijden_verdiepend(self):
        'Een granuleerdere beeld van een competitie uitvoeren dmv Poisson verdeling'
        for home_team in self.teams: # for each team , each team will play as hometeam
            for away_team in self.teams:# get the list of the restof the teams -> oponents/away_teams
                if home_team.name != away_team.name:
                    ht_point, at_point = self.match_outcome(home_team, away_team) # pakt de doelpunten                    
                    
                    # Voeg de doelsaldo toe
                    home_team.doelsaldo += ht_point - at_point 
                    away_team.doelsaldo += at_point - ht_point
                    
                    # Voeg de scores toe 
                    if ht_point > at_point:
                        home_team.score += 3
                    elif ht_point < at_point:
                        away_team.score += 3
                    else: # ht_points == at_points
                        home_team.score += 1
                        away_team.score += 1
    
    
    def wedstrijden_prob_list(self):
         'Een competitie uitvoeren met gegeven lijsten van win/gelijk/verlies van de teams'
         for home_team in self.teams: # for each team , each team will play as hometeam
            for away_team in self.teams:# get the list of the restof the teams -> oponents/away_teams
                if home_team.name != away_team.name:
                    random_number = self.rng.randdec()  #  pakt random getal
                    prob_lst = list(map(lambda x: x/100, home_team.prob_list_teams[away_team.name]))
                    
                    # Voeg de scores toeg
                    if  random_number < prob_lst[2]: # rn < 18 , dan verlies thuisspelende partij
                        away_team.score += 3
                    elif random_number < (prob_lst[2] + prob_lst [1]): # rn zit tussen 18 en  35 (18+17), dan is er een gelijkspel
                        home_team.score += 1
                        away_team.score += 1
                    else: # rn zit tussen 35 en 100 (35 + 65), dan win de thuisspelende partij
                        home_team.score += 3 
    
    def rankings(self):
        'Sorteer teams op base van score en doelsaldo'
        return reversed(sorted(self.teams, key =lambda x : (x.score,x.doelsaldo)))

    def reset(self):
        'Zet doelsaldo en score van alle team om naar 0'
        for i in self.teams:
            i.doelsaldo = 0
            i.score = 0
    
    