import random

# identify and isolate system 
'''
This will start once a critical threshold of cases is hit (different for each city) but chance for it
to happen before hand but not to happen if no cases have hit 

Not just for infected also for people travelling to different cities if the city has 
a quarantine rule for arrivals

Factors of Testing (identify):
    - persons willing ness to be tested 
    - accuracy of those tests 
    - accuracy of the doctors taking those tests which should be a negative exponential as the day increases accuracy decreases

also have some sort of track and trace system 
where once someone is identified then recently encounted people are also isolated 
that would be a queue FIFO so first in contact once x time has reached leaves first 
'''

def identify(person):
    # chance to not identify infected people 
    if numbCases == criticalThresholdOfCases:
        if infected.getNumbDaysInfected == quarantineDayAfterInfection:
            quarantine(person)
       
def quarantine(person):
    if (person.status == 'I') and (not person.getSymptomatic) and (person.getNumbDaysInfected >= quarantineInfectedDays): 
        person.setQuarantine(True)
    elif ((person.getLastMapID != map.getMapID) and (person.getDaysSpent =< quarantineSusceptibleDays)):
        person.setQuarantine(True)

# social distancing system
'''
social distance factor
repulsive force between people

factors of it:
    - person cares or not 

or could be perctage based so x% of population abide by it 
'''
def movement():
    if socialDistanceFactor > 0:
        pass

# transmisson system
'''
Transmisson between people

Chance to leave a trace which is infected person leaving infection on the position they are currently on
this will fade away and decrease in transmitabliltiy as time goes on  
'''
def set_status():
    # determins whether a newley infected person is symptomatic or asymptomatic 
    if random.random() < p_asymptomatic_on_infection:
        asymptomatic = False

def transmission():
    pass

# travel system
'''
travel rate which is a percentage of the chance for a person every day to travel to a different community 
when they get there they either 
spawn at the centre of the map which is where the airport is located 

'''
# these people will be itterated over out side of the simulation loop 
def travel():
    if travelRate < random.random():
        # function returns all map ids apart from current map id   
        newMapID = random.choice(getMapIDs(person.getPopulationID).split())
        person.setPopulationID(0)
        person.setTravellingTo(getMapPopulation(newMapID))
        person.setTravel(True)
        person.setRequiredTravelTime(getMapTravelTime(newMapID))

# simulation handler call the simulation again but using the travelling map as well as the calling travelling function 
# instead of the day 
def updateDB():
    updateTravelTime(person.getID)

def travelling():
    #also update infected peoples times 
    for person in map.getPopulation():
        # increase travel time by a day 
        person.setTravelTime()
        updateDB()


# travel restrictions system 
'''
This also works with the quarantine system

Five types of travel restrictions:
    - No travel 
    - Only travel for people born there 
    - Only travel for people born there but with quarantine 
    - Open travel but with quarantine 
    - Open travel 

'''

# Central hubs
'''
buildings where people travel to 
such as school or office or shops or just a central hub that includes those things

factors:
    - work frequency 
    - shopping frequency 
'''

# antiviral therapeutics system
'''
some drug that can reduce infection time 
'''

# working out reproductive number 
'''
infected person count how many people they infect , the average of this amount out of everyone who has been sick 
is equal to the effective reproductive number

basic reproductive number R0 at the very beginning so for the first person infected 
'''