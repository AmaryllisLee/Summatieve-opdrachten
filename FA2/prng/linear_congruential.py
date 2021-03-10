class LCR:
    
    def __init__(self, a, c, m, seed):
        self.a = a
        self.c = c
        self.m = m
        self.seed = seed
        
    def random_number_generator(self):
        "Generating a random number using linear congruential method " 
        next_seed = (self.a * self.seed + self.c) % self.m
        self.seed = next_seed 
        return next_seed  # convert to number between 0 -99
    
    def randdec(self):
        "Convert generated randomn number in to a decimal number"
        return self.random_number_generator()/self.m # convert to number between 0 and 1
    
