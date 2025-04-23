
from constants import SEEKPOWERPELLET,SEEKGHOST, FLEE 
from pacman import *
import csv
import os



class StateMachine(object):
    def __init__(self, pacman):
        self.pacman = pacman
        self.time = 7
        self.csv_name = "pacman_training_data.csv"
        self.fieldnames = [
            "ghost_close",
            "pellet_eaten",
            "closePP",
            "state_time_left",
            "pacman_state"
            ]
        
        
    # Checks if the closest ghost is closer than some threshold
    def ghostClose(self,distance):
        res = False
        for ghost in self.pacman.ghosts:
          dist = self.pacman.dist(ghost.node.position.asTuple(),self.pacman.position.asTuple())
          if dist < distance:
            res = True
        return res
    
    # Checks if the closest power pellet is closer than some threshold
    def pelletClose(self,distance):
        if not self.pacman.powerPellets:
            return False
        
        PP = self.pacman.nearbyPowerPellet()
        dist = self.pacman.dist(PP.position.asTuple(),self.pacman.position.asTuple())
        if dist < distance:
            return True
        return False





 
      
    # Checks for events and changes pacman states according to event
    def checkEvent(self, dt):
        self.pacman.updatePowerPellets()
        
        # Eaten pellet
        pelletEaten = self.pacman.eatPellets(self.pacman.allPowerPellets)  
        pelletEatenBool = pelletEaten is not None
        
        #Bool: ghost distance < threshold
        close = self.ghostClose(100)
        
        #Bool: power pellet distance < threshold
        closePP = self.pelletClose(150)
        
        
        
        #seek power pellet if its close
        if closePP:
            self.pacman.myState = SEEKPOWERPELLET
            self.observe_and_log(close, pelletEatenBool,closePP,self.time)
            
        
            
        # If pacman eats power pellet, seek ghost
        if pelletEaten is not None and pelletEaten.alive:
            pelletEaten.alive = False
            self.pacman.myState = SEEKGHOST
            self.observe_and_log(close, pelletEatenBool ,closePP,self.time)
            self.time = 6  # Seek time
            
            
            

        # Count down time or stop seeking ghost
        if self.pacman.myState == SEEKGHOST:
            self.time -= dt  
            self.observe_and_log(close, pelletEatenBool,closePP,self.time)
            
            if self.time <= 0:
                self.pacman.myState = SEEKPELLET
                self.observe_and_log(close, pelletEatenBool,closePP,self.time)
                self.time = 6  # Seek time
                

        # Check distance to closest ghost and if true, FLEE
        if close and self.pacman.myState not in [SEEKGHOST, FLEE]:
            self.pacman.myState = FLEE
            self.observe_and_log(close, pelletEatenBool,closePP,self.time)
            self.time = 6  # Seek time
            self.flee_time = 6  # Reset FLEE-tid


        # If flee-state, check if we should stop
        if self.pacman.myState == FLEE:
            self.flee_time -= dt
            if self.flee_time <= 0 or not close:
                self.pacman.myState = SEEKPELLET
                self.observe_and_log(close, pelletEatenBool, closePP,self.time)
                
                
                
          
          
    
    # Logging data for decision tree training 
        
    
        
        
    def init_csv(self):
        if not os.path.exists(self.csv_name) or os.path.getsize(self.csv_name) == 0:
            with open(self.csv_name, mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()
                

    def log_state(self,feature_dict):
        with open(self.csv_name, mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(feature_dict)
            
            
    def categorize_time(self, time):
        if time <= 1:
            return 0
        return 1
    

    def observe_and_log(self, ghost_close, pellet, closePP, state_time_left):
        data = {
            "ghost_close" : ghost_close,
            "pellet_eaten" : pellet,
            "closePP" : closePP,
            "state_time_left" : self.categorize_time(state_time_left),
            "pacman_state" :  self.pacman.myState,
        }
        
        self.log_state(data)
        
    
    
        
          
            
            
            
            
    
    

            
                    
        
        
        