import math
import random

class Population():
    def __init__(self, data):
        self.data = data

        results = calcStatistics(self.data, False)
        self.mean = results[0]
        self.var = results[1]
        self.std = results[2]
        self.mode = results[3]
        self.median = results[4]
        
    def ZCI_2Tail(self, confidence):
        if confidence == 95:
            return [self.mean - 1.96 * self.std / len(self.data), self.mean + 1.96 * self.std / len(self.data)]
        elif confidence == 99:
            return [mean - 2.576 * self.std / len(self.data), mean + 2.576 * self.std / len(self.data)]
        else confidence == 90:
            return [mean - 1.645 * self.std / len(self.data), mean + 1.645 * self.std / len(self.data)]

    def ZCI_1Tail(self, confidence):
        if confidence == 95:
            return [self.mean - 1.645 * self.std / len(self.data), self.mean + 1.645 * self.std / len(self.data)]
        elif confidence == 99:
            return [mean - 1.96 * self.std / len(self.data), mean + 1.96 * self.std / len(self.data)]
        else confidence == 90:
            return [mean - 1.28 * self.std / len(self.data), mean + 1.28 * self.std / len(self.data)]

    def PDF(self, mean):
        constant = 1 / (self.std * (2 * math.pi) ** .5)
        exponent = -(mean - self.mean) / (2 * self.var)
        return constant * math.exp(exponent)

    def zScore(self, dpoint):
        pass
    
class Sample(Population):

    def __init__(self, data, population = None):
        self.originalData = data
        self.resetData(data)

        self.population = population

    def correctStatistics(self, overwrite = False):
        if overwrite:
            self.data = removeOutliers(self.data)
            self.resetData(self.data)
        else:
            correctedData = removeOutliers(self.data)
            return correctedData
            
    def resetData(self, data = self.originalData):
        self.data = data
        results = calcStatistics(self.data, True)
        self.mean = results[0]
        self.var = results[1]
        self.std = results[2]
        self.mode = results[3]
        self.median = results[4]
        self.df = len(data)
        
        
def calcStatistics(data, sample = True):
    m = mean(data)
    v = var(data, sample)
    s = std(data, sample)
    mo = mode(data)
    me = median(data)
    
    return [m,v,s,mo,me]

def mean(data):
    return sum(data) / len(data)

def var(data, sample = False):
    mean = calcMean(data)
    return sum([(x - mean) ** 2 for x in data]) / (len(data) - sample)

def std(data, sample = False):
    return calcVar(data, sample) ** .5

def median(data):
    sort = sorted(data)

    if len(data) % 2 != 0:
        return data[int(len(data) / 2)]
    else:
        return (data[len(data) / 2] + data[len(data) / 2 + 1]) / 2 
    
def mode(data):
    counts = [data.count(x) for x in data]
    return data[counts.index(max(counts))]

def bayes(p0,p1,p2): # returns prob of p0 given p1 where p1 = p1 | p0 and p2 = p1 | not p0
    return (p0 * p1) / (p0 * p1 + (1 - p0) * (p2)) 

def quartiles(data):
    lowerRange = (len(data) + (len(data) % 2 != 0)) / 4
    upperRange = 3 * (len(data) + (len(data) % 2 != 0)) / 4
    lq = [data[x] for x in range(0, lowerRange + 1)]
    mq = [data[x] for x in range(lowerRange + 1, upperRange)]
    uq = [data[x] for x in range(upperRange, len(data))]

    return [lq, mq, uq]

def iQRange(data):
    quartiles = quartiles(data)
    return quartiles[2][0] - quartiles[0][-1]

def calcOutliers(data):
    r = 1.5 * iQRange(data)
    m = mean(data)
    return [x for x in data if abs(x - m) > r]

def removeOutliers(data):
    outliers = calcOutliers(data)
    for x in outliers:
        data.remove(x)

    return data

def binomial(prob, trials, successes):
    A = math.factorial(trials) / (math.factorial(successes) * math.factorial(trials - successes))
    B = prob ** sucesses * (1-prob) ** (trials - successes)
    return A * B

def randomSample(population, size):
    data = population.data
    sample = []
    for x in range(size):
        sample.append(data[random.randint(0, len(data) - 1)])
        
    sample = Sample(sample, population)
    return sample


def covar(sample1, sample2):
    mean1 = sample1.mean
    mean2 = sample2.mean
    return sum[(x - mean1) * (y - mean2) for x,y in list(zip(sample1.data, sample2.data))]

def rTest(sample1, sample2):
    if len(sample1.data) != len(sample2.data):
        raise Exception('Samples must be of equal length')
    
    length = len(sample1)
    numer = covar(sample1, sample2) * length
    denom = math.sqrt(sample1.var * length + sample2.var * length)

    return numer / denom

def cohenD(sample1, sample2): #assumes they have the same std
    return (sample1.mean - sample2.mean) / sample1.std 

if __name__ == "__main__":
        
