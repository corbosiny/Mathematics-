from __future__ import division
from vector import Vector
import sys
import matrix

class Line(): #deals with lines of the form Ax + By = k, then paramaeritizes them in 3D of the form basepoint + t<direction vector> 

    def __init__(self, normalVector= [0,0], constant = 0, tolerance = .01, dp = 3):
        self.normalVector = Vector(normalVector, tolerance, dp)
        self.constant = constant
        self.tolerance = tolerance
        self.dp = dp
        
        if constant != 0: #just parameritizes the line as a base point then a vector dependant on time
            index = self.firstNonZero()
            basePointCoor = [0] * len(normalVector)
            basePointCoor[index] = round(constant / normalVector[index], dp)
            self.basePoint = Vector(basePointCoor, tolerance, dp)

        else:
            self.basePoint = Vector()
        
        
    def parallel(self, line): #determines if one is scalar multiple of the other by comparing variable ratios
        return self.normalVector[0] / line.normalVector[0] ==  self.normalVector[1] / line.normalVector[1]

    def perp(self, line):
        return self.normalVector.dotProduct(line.normalVector)>= -1 - self.tolerance and self.normalVector.dotProduct(line.normalVector)<= -1 + self.tolerance

    def intersection(self, line):
        if self.parallel(line) and self != line: #if they are parallel but not the same line then no intersection
            return None
        elif self == line: #if they are the same line(even scalar multiples) then infinite intersections
            return 'INFINITE'

        else:
             #otherwise we use our handy dandy matrix solver
            newMatrix = matrix.Matrix([[self.normalVector[0], self.normalVector[1]], [line.normalVector[0], line.normalVector[1]]])
            newSolutions = matrix.Matrix([[self.constant], [line.constant]])
            newMatrix, solutions = newMatrix.equationSolver(newSolutions)
            if not isinstance(solutions, str):
                solutions = [solutions[0][0], solutions[1][0]]
            return solutions 
            
    #everything below is just for scalar operations on the line, easy to understand one line functions
    def __eq__(self, line):
        return self.normalVector[0] / line.normalVector[0] == self.normalVector[1] / line.normalVector[1] == self.constant / line.constant

    def __add__(self, b):
        if isinstance(b, int) or isinstance(b, float):
            return Line(self.normalVector.coor, self.constant + b, self.tolerance, self.dp)
        else:
            raise ValueError("Unsupported operation between Line and %s" % type(b))

    def __sub__(self, b):
        if isinstance(b, int) or isinstance(b, float):
            return Line(self.normalVector.coor, self.constant - b, self.tolerance, self.dp)
        else:
            raise ValueError("Unsupported operation between Line and %s" % type(b))

    def __mul__(self, b):
        if isinstance(b, int) or isinstance(b, float):
            return Line([x * b for x in self.normalVector], self.constant * b, self.tolerance, self.dp)
        else:
            raise ValueError("Unsupported operation between Line and %s" % type(b))

    def __truediv__(self, b):
        if isinstance(b, int) or isinstance(b, float):
            return Line([ x / b for x in self.normalVector], self.constant + b, self.tolerance, self.dp)
        else:
            raise ValueError("Unsupported operation between Line and %s" % type(b))

    def __floordiv__(self, b):
        if isinstance(b, int) or isinstance(b, float):
            return Line([ x / b for x in self.normalVector], self.constant + b, self.tolerance, self.dp)
        else:
            raise ValueError("Unsupported operation between Line and %s" % type(b))

    def __iter__(self):
        return self.normalVector.coor
    
    def __getitem__(self, key):
        return self.normalVector.coor[key]

    def firstNonZero(self):
        for index, num in enumerate(self.normalVector.coor[0:2]):
            if abs(num) > 0 + self.tolerance:
                return index

        raise Exception('No Non-Zero Coefficients')
    
    def __str__(self): #looks complex but its just organizing our equation in a pretty form
        msg = ""
        if self.normalVector[0] % 1 == 0: #if an int print as an int, otherwise print as a float
            msg += "(%d)X " % self.normalVector[0]

        else:
            msg += "(%.2f)X " % self.normalVector[0]

        if self.constant % 1 == 0:              
            if self.constant > 0:
                msg += "+ %d " % self.constant
            else:
                msg += "- %d " % abs(self.constant) #if it is negative we put a negative then the abs form to avoid two negatives in the string
        else:
            if self.constant > 0:
                msg += "+ %.2f " % self.constant
            else:
                msg += "- %.2f " % abs(self.constant)

        if self.normalVector[1] % 1 == 0:
            msg += "= (%d)Y" % self.normalVector[1]

        else:
            msg += "= (%.2f)Y" % self.normalVector[1]

        return msg

if __name__ == "__main__":  #just test code
    l1 = Line([4.046, 2.836], 1.21)
    lpl = Line([8.172, 4.114], 9.883)
    lpp = Line([-.5,0], 2)
    l2 = Line([4.046 * 2, 2.836 * 2], 1.21 * 2)
    print(l1 == l2)
