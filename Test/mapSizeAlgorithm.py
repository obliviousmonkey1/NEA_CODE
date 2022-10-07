populationSize = 400

# algorithm for generating map size 


def factors(n, i, ):
    if i > n:
        return []
    else:
        if (n % i) == 0:
            return [i] + factors(n,i+1)
        else:
            return factors(n,i+1)

def generateMapSize(populationSize):
    a = factors(populationSize,1)
    width = a[len(a)//2]
    height = populationSize//width
    print(f'width {width}, height {height}')


generateMapSize(populationSize)