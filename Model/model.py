import pandas as pd
import numpy as np
import random 

class Pursuit:
    def __init__(self,Vocabulary,gamma,smoothing_factor,treshold,change_Denominator = False): #Add vocab manually so that it can be used for already existing vocabulary too.
        self.Vocabulary = Vocabulary   
        self.gamma = gamma 
        self.smoothing_factor = smoothing_factor
        self.treshold = treshold
        self.observed_Meanings = []
        self.Uttered_dict = {}
        self.Visible_dict = {}
        self.Favories = {}
        self.change_Denominator = change_Denominator

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
            self.update(uttered,select,self.gamma)
            return
        else:
            self.update(uttered,choice,self.gamma)

    
    def update(self,uttered,visible,update): 
        self.Uttered_dict.setdefault(uttered, {})[visible] = update
        self.Visible_dict.setdefault(visible, {})[uttered] = update
    def fix_Favorite(self,uttered): #Takes uttered word
        if uttered not in self.Favories:
            maxim = max(self.Uttered_dict[uttered].values())
            item = [i for i,v in self.Uttered_dict[uttered].items() if v == maxim][0]
            self.Favories[uttered] = item


    def reward(self,uttered,hypothesis): #Takes uttered word and hypothesis. 
        current = self.Uttered_dict[uttered][hypothesis]
        update = current + self.gamma * (1 - current)
        self.update(uttered=uttered,visible=hypothesis,update=update)
    


    def penalize(self,uttered,hypothesis):
        current = self.Uttered_dict[uttered][hypothesis]
        update = current * (1 - self.gamma)
        self.update(uttered=uttered,visible=hypothesis,update=update)
    
    def check_Pursuit(self,uttered,hypothesis,change_Denom = None, vis = None):
        if change_Denom is None:
            change_Denom = self.change_Denominator
        if change_Denom is False:
            current = self.Uttered_dict[uttered][hypothesis]
            P = (current + self.smoothing_factor) / (sum(self.Uttered_dict[uttered].values()) + len(self.observed_Meanings) * self.smoothing_factor)
        else:
            current = self.Uttered_dict[uttered][hypothesis]
            P = (current + self.smoothing_factor) / (sum(self.Uttered_dict[uttered].values()) + len(vis) * self.smoothing_factor)

        if P >= self.treshold:
            return True
        else:
            return False


    
    def set_Vocabulary(self,Dataframe,get_Vocab = False):
        #Convert them to list
        uttered_Data = Dataframe["uttered"].tolist()
        visible_Data = Dataframe["visible"].tolist()

        for i in range(len(uttered_Data)):
            for j in  range(len(uttered_Data[i])):
                uttered_Word = uttered_Data[i][j]
                visible_List = visible_Data[i]
                for k in visible_List:
                    if k not in self.observed_Meanings:
                        self.observed_Meanings.append(k)

                if uttered_Word not in self.Uttered_dict:
                    self.initialize(uttered=uttered_Word,L_visible=visible_List)
                    self.fix_Favorite(uttered_Word)
                
                else:
                    hypo = self.Favories[uttered_Word]
                    
                    if hypo in visible_List:
                        self.reward(uttered_Word,hypo)
                        if self.check_Pursuit(uttered_Word,hypo,vis = visible_List):
                            self.Vocabulary[uttered_Word] = hypo 
                    else:
                        self.penalize(uttered_Word,hypo)

                        new_poss_hypo = random.choice(visible_List)

                        if new_poss_hypo not in self.Uttered_dict[uttered_Word]:
                            self.update(uttered=uttered_Word,visible=new_poss_hypo,update=self.gamma)
                            self.fix_Favorite(uttered=uttered_Word)
                        else:
                            self.reward(uttered=uttered_Word,hypothesis=new_poss_hypo)
                            self.fix_Favorite(uttered=uttered_Word)
        if get_Vocab:
            return self.Vocabulary
    def get_Results(self,Gold,get_Score = False,Compare = False):
        score = 0
        over = len(Gold)
        for uttered in Gold:
            if uttered in self.Vocabulary:
                if self.Vocabulary[uttered] == Gold[uttered]:
                    score += 1
                    if Compare == True:
                        print(f"[TRUE:[{uttered}] in Vocab: {self.Vocabulary[uttered]} || in gold set: {Gold[uttered]}]")
                else:
                    if Compare == True:
                        print(f"[FALSE:[{uttered}] in Vocab: {self.Vocabulary[uttered]} || in gold set: {Gold[uttered]}]")
        print(f"{int((score/over)*100)}% Accuracy")

        if get_Score:
            return int((score/over)*100)
    
    @staticmethod
    def text_to_df(name):
        with open(f'Data/{name}/{name}.txt', 'r') as file:
            lines = file.readlines()
        uttered = []
        visible = []
        row = 0
        while row < len(lines):
            uttered.append(lines[row].split())
            visible.append(lines[row+1].split())
            row +=3
        return pd.DataFrame({
            "uttered" : uttered,
            "visible" : visible
        })
    

    @staticmethod
    def csv_to_dict(name):
        df = pd.read_csv(f'Data/{name[:len(name)-5]}/{name}.csv')
        train = {}

        for i in range(len(df)):
            train[df.iloc[i, 0]] = df.iloc[i, 1]
        return train

        
        




                            




                







        

    

    
    







    



    


                



        
        
        