from voetbal.teams import Team
from voetbal.tournament import Tournament

import numpy as np
import pandas as pd
from IPython.display import display # toon datafram aan in de vorm van ee tabel

def MC(n, rng, keuze):
    # generate dict of average ranking of the teams
    average_ranks = {}
    
    # Creer Tournament en voeg Team objecten 
    t = Tournament(rng)
    t.teams.append(Team("ajax", 3.2, 0.9, 3.1, 0.6, 
                        {"feyenoord":[65,17,18], "psv":[54,21,25], "fcutrecht":[74,14,12], "willemII":[78,13,9]}))
    t.teams.append(Team("feyenoord", 2.4, 1.1, 2.2, 0.8, 
                       {"ajax": [30,21,49], "psv":[37,24,39], "fcutrecht":[51,22,27], "willemII":[60,21,19]}))
    t.teams.append(Team("psv", 2.1, 0.7, 1.8, 1.3, 
                       {"ajax": [39,22,39], "feyenoord":[54,22,24], "fcutrecht":[62,20,18], "willemII": [62,22,16]}))
    t.teams.append(Team("fcutrecht", 1.9, 1.2, 3, 2.4,
                      {"ajax":[25,14,61], "feyenoord": [37,23,40], "psv":[29,24,47], "willemII": [53,23,25]} ))
    t.teams.append(Team("willemII", 1.4, 1.7, 1, 1.5,
                        {"ajax": [17, 18, 65], "feyenoord":[20,26,54], "psv":[23,24,53], "fcutrecht":[37,25,38]}))
    
    # dictionary di bevat alle teams en hun ranking (positie 1 tot 5) in n competitie
    for team in t.teams:
        average_ranks[team.name] = {}
        for pos in range(1, len(t.teams)+1):
            average_ranks[team.name][pos] = 0
    
    # Vour uit wedstrijden n keren 
    for i in range(0, n):
        if keuze == 'probability list':
            t.wedstrijden_prob_list()
        elif keuze == 'verdiepend':
            t.wedstrijden_verdiepend()
        
        # Voeg rankingstoe in dictionary
        pos = 1
        for team in t.rankings():
            average_ranks[team.name][pos] +=1
            pos+=1
        
        t.reset() # doelsaldo en scores van de teams resetten.
            
        
    # Geeft dictionary weer in een dataframe
    df = pd.DataFrame(average_ranks).apply(lambda x: x/n *100)
    display(df)
    
    
    