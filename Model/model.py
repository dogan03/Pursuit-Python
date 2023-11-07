import pandas as pd
import numpy as np
import random 

class Pursuit:
    def __init__(self,Vocabulary,gamma):
        self.Vocabulary = Vocabulary   
        self.gamma = gamma 
        self.Uttered_dict = {}
        self.Visible_dict = {}

    def initialize(self,uttered,L_visible): # Takes word and List of VISIBLE elements(and dict which is defined within class). Returns chosen one.
        a = float("inf")
        l = []
        
        for visible in L_visible: 
            if visible not in self.Visible_dict: 
                l.append(visible)
            else:
                b = max(self.Visible_dict[visible].values())
                if b < a:
                    a = b
                    choice = visible
        if l != []:
            select = random.choice(l)
            
            self.initialize_update(uttered,select)
            return
        else:
            self.initialize_update(uttered,choice)
    def initialize_update(self,uttered,visible):
        if uttered not in self.Uttered_dict:
            self.Uttered_dict[uttered] = {visible : self.gamma}
            if visible not in self.Visible_dict:
                self.Visible_dict[visible] = {uttered: self.gamma}
            else:
                self.Visible_dict[visible][uttered] = self.gamma
        else:
            self.Uttered_dict[uttered][visible] = self.gamma
            if visible not in self.Visible_dict:
                self.Visible_dict[visible] = {uttered: self.gamma}
            else:
                self.Visible_dict[visible][uttered] = self.gamma






    



    


                



        
        
        