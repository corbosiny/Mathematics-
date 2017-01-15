from gaussian import Gaussian
import math

def mean(nums):
    return sum(nums) / len(nums)

def variances(nums):
    mu = mean(nums)
    variances = [math.pow(x - mu, 2) for x in nums]
    return variances

def var(nums):
    var = variances(nums)
    var = mean(var)
    return var

def stdEvs(nums):
    var = variances(num)
    stdEvs = [math.sqrt(x) for x in var]
    return stdEvs

def stdEv(nums):
    return math.sqrt(var(nums))

def zScores(nums):
    mu = mean(nums)
    std = stdEv(nums)
    scores = [(x - mu) / std for x in nums]
    return scores

def evalZscore(score):
    gauss = Gaussian(1)
    return gauss.returnProbDensity

def evalZscores(scores):
    pScores = [evalZscore(x) for x in scores]        
    return pScores

def pScores(nums):
    mu = mean(nums)
    variance = var(nums)
    gauss = Gaussian(var, mu)    
    pScores = [gauss.returnProbDensity(x) for x in nums]
    return pScores

def returnProbs(nums):
    mu = mean(nums)
    variance = var(nums)
    gauss = Gaussian(variance, mu)
    probs = [gauss.evaluate(x) for x in nums]
    return probs

def pTest():
    pass

def anovaTest(samples):
    pass

if __name__ == "__main__":
    
