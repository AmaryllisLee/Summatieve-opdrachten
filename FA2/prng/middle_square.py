class MiddleSquare:
    
    def __init__(self, seed):
        self.size = len(str(seed)) # pakt de lengte van  de seed
        self.seed = seed # starting value
        
        
    def random_number_generator(self):
        "Generating random number using middle square method"
        x = str(self.seed**2) 
        if len(x) != (self.size*2):
            x = x.zfill(self.size*2)
        
        y= int(self.size/2)
        self.seed = int(x[y: y + self.size]) 
        return self.seed
        
    def randdec(self):
        "Convert random number in to a decimal number"
        return self.random_number_generator()/10**self.size
    