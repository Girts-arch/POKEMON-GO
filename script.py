typeAdvantages={
    "Fire": ["Grass", "Ice"],
    "Water": ["Fire", "Rock"],
    "Grass": ["Water", "Rock"],
    "Ice": ["Grass"],
    "Rock": []
}

evolutions={
    "Charmander":[16, "Charmeleon"],
    "Charmeleon":[36, "Charizard"],

}

class Pokemon:
    def __init__(self, name, level, pokeType, faint=False):
        self.name=name
        self.type=pokeType
        self.level=level 
        if level>100:
            self.level=100
        self.maxHealth=level*5
        self.currentHealth=self.maxHealth
        self.isFaint=faint
        self.experience=0 # will keep threshold of level*2 for leveling up
        self.nextEvolution=-1 #if there's no next evo, keep this at -1 else set it to the level of the next evolution
        if self.name in evolutions:
            self.nextEvolution=evolutions[self.name][0]

    def knockOut(self):
            self.currentHealth=0
            self.isFaint=True 
            print(f"{self.name} fainted!")
    
    def loseHealth(self, damage):
        #Health cannot go below 0
         if self.currentHealth-damage<=0:   
            self.knockOut()
         else:
             self.currentHealth-=damage
             print(f"{self.name} now has {self.currentHealth} health!")
    
    def gainHealth(self, recovery):
        #Health cannot go over max health
         if recovery+self.currentHealth>=self.maxHealth:
             self.currentHealth=self.maxHealth
         else:
            self.currentHealth+=recovery
         print(f"{self.name} now has {self.currentHealth} health!")
    
    def revive(self):
        #In games, the revived pokemon usually gets half its health restored
        self.currentHealth=self.maxHealth/2
        self.isFaint=False
        print(f"{self.name} has been revived. It now has {self.currentHealth} health!")

    def levelUp(self, remainingExp=0):
        #level up, if I reach an evolution, evolve my poke
        self.level+=1
        self.experience=remainingExp
        print(f"{self.name} leveled up! It's now at level {self.level}.")
        if self.nextEvolution!=-1 and self.level>=self.nextEvolution:
            self.evolve()
    
    def evolve(self):
        #Get the evolved pokemon name, change name to that and check if there's any further evolution
        #then store that level next e.g charmander evolves into Charmeleon
        #now Charmeleon's next evolution var will have 36 as the level for Charizard evo
        evolutionName= evolutions[self.name][1]
        oldName=self.name 
        if evolutionName in evolutions:
            self.nextEvolution= evolutions[evolutionName][0]
        else:
            self.nextEvolution=-1
        self.name=evolutionName
        print(f"{oldName} evolved into {self.name}!")

    def gainXP(self, otherPokeLevel):
        #XP gained will be 0.25* level of the other pokemon I beat
        self.experience+= 0.25*otherPokeLevel
        threshold=self.level*2
        print(f"{self.name} gained {0.25*otherPokeLevel} experience from the battle!")
        if self.experience>= threshold:
            self.levelUp(self.experience-threshold)
        
    
        
    
    
    def attack(self, enemy):
        #Dealing with Water, Fire, Grass, Ice, and Rock types
        damage=0
        #Attack according to type advantage, the dictionary defining them is declared at the top

        if self.isFaint:
            print(f"{self.name} has fainted, it cannot attack! Please Switch Pokemon")
            return 
        if enemy.type in typeAdvantages[self.type]:
            #do double damage
            damage=self.level*2

        elif self.type in typeAdvantages[enemy.type]:
            #do half damage
            damage=self.level/2
        else:
            #do normal damage
            damage=self.level
        
        print(f"{self.name} attacked {enemy.name} and dealt {damage} damage!")
        enemy.loseHealth(damage)

    def printStats(self):
        print(f"Name: {self.name}, Level: {self.level}, Max Health: {self.maxHealth}, Current Health: {self.currentHealth}.")

    
    def __repr__(self):
        return f"{self.name}"

class Trainer:
    def __init__(self,name,numPotions, pokeTeam):
        self.name=name 
        self.numPotions=numPotions
        self.currPoke=0 #index in the list, initially we take the first pokemon
        self.pokeTeam=pokeTeam
        
    def usePotion(self):
        if self.numPotions>0:
            print(f"{self.name} used a Potion!")
            self.pokeTeam[self.currPoke].gainHealth(20)
            
        else:
            print(f"{self.name} doesn't have any potions left!")
    
    def attackOther(self, otherTrainer):
        #get pokemon using other's currPoke index from their team and attack that poke
        self.pokeTeam[self.currPoke].attack(otherTrainer.pokeTeam[otherTrainer.currPoke])

    def switchPoke(self, pokeToSwitch):
        #pokeToSwitch is a name 
        #Get corresponding pokemon from team, if it doesn't exist, raise the error
        #otherwise switch pokemon
        pokemon=None
        for x in self.pokeTeam:
            if x.__repr__()==pokeToSwitch:
                pokemon=x
                break
                
        if pokemon==None:
            print(f"{pokeToSwitch} is not in your team!")
        elif pokemon.isFaint:
            print(f"{pokeToSwitch} has fainted, can't switch to it.")
        else:
            self.currPoke= self.pokeTeam.index(pokemon)
            print(f"{self.name} switched to {pokemon}")
        
    def printCurrPoke(self):
        print(f"{self.name}'s Current Active Pokemon: {self.pokeTeam[self.currPoke]}")

    def checkAllFainted(self): #For future use: if i implement a battle
        for poke in self.pokeTeam:
            if poke.isFaint==False:
                return False 
        return True 


class Charmander(Pokemon):
    def __init__(self, specialMove, level=5):
        super().__init__("Charmander", level, "Fire")
        self.specialMove= specialMove
    
    def attack(self, enemy): #First display its special move, then call the original parent function
        print(f"{self.name} used {self.specialMove}!")
        super().attack(enemy)




####Testing
#Pokemon("Charizard", 50, "Fire")

#Initialize two trainers with two pokes each
jeffsPoke=[Charmander("Flamethrower",15), Pokemon("Swampert", 50, "Water")]
jeff= Trainer("Jeff", 5, jeffsPoke ) #5 potions
bobsPoke=[Pokemon("Venasaur", 50, "Grass"), Pokemon("Onyx", 50, "Rock")]
bob= Trainer("Bob",0, bobsPoke) #0 potions

jeff.printCurrPoke()
print("Jeff's Current Pokemon")
for poke in jeff.pokeTeam:
    poke.printStats()

print("Bob's current Pokemon")
for poke in bob.pokeTeam:
    poke.printStats()

#Jeff attacks gary who then attacks back, jeff uses a potion
jeff.attackOther(bob)
bob.usePotion() #He has 0 so he wont be able to!
bob.attackOther(jeff)
jeff.usePotion()
#we level up charmander and see its evolution
jeffsPoke[0].levelUp()
jeff.printCurrPoke() #print current pokemon to see updated evolved pokemon

jeff.switchPoke("Swampert") 
jeff.printCurrPoke() #print current pokemon after switching 

#same for bob
bob.printCurrPoke() 
bob.switchPoke("Onyx")
bob.printCurrPoke()
