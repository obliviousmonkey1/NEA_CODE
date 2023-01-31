populationSize = 100

# algorithm for generating map size 


def addOne(i):
        return i + 1 

def factors(f, n, i):
    if i > n:
        return []
    else:
        if (n % i) == 0:
            return [i] + factors(f, n, f(i))
        else:
            return factors(f, n, f(i))
            
def generateMapSize(populationSize):
    a = factors(addOne, populationSize, 1)
    width = a[len(a)//2]
    height = populationSize//width
    print(f'width {width}, height {height}')


generateMapSize(populationSize)

  
