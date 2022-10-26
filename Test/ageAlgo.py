from random import random, randint

def calcuateAge() -> int:
    chance = random()
    if chance < 0.21:
        return randint(10,18)
    elif chance > 0.21 and chance < 0.5:
        return randint(18,39)
    elif chance > 0.5 and chance < 0.77:
        return randint(40,59)
    elif chance > 0.77:
        return randint(60,80)
    
age = calcuateAge()
print(age)
print(1-((age/100)**5))