from vector import Vector
import sys
class Line(): #deals with lines of the form Ax + By = k, then paramaeritizes them in 3D of the form basepoint + t<direction vector> 

    def __init__(self, normalVector= [0,0,0], constant = 0, tolerance = .01, dp = 3):
        self.normalVector = Vector(normalVector, tolerance, dp)
        self.constant = constant
        
        if constant != 0:
            index = Line.firstNonZero(normalVector, tolerance)
            basePointCoor = [0] * len(normalVector)
            basePointCoor[index] = round(constant / normalVector[index], dp)
            self.basePoint = Vector(basePointCoor, tolerance, dp)

        else:
            self.basePoint = Vector()
        
        self.tolerance = tolerance
        self.dp = dp
        
    def parallel(self, line):
        return self.normalVector.parallel(line.normalVector)

    def perp(self, line):
        return abs(self.normalVector.dotProduct(line.normalVector)) <= 0 + self.tolerance

    def intersection(self, line):
        if self.parallel(line) and self != line:
            return None
        elif self == line:
            return 'INFINITE'

        else:
            try:
                indicies1 = [0, 0]
                indicies2 = [0, 0]
                
                indicies1[0] = Line.firstNonZero(self.normalVector.coor, self.tolerance)
                indicies1[1] = Line.firstNonZero(self.normalVector.coor[indicies1[0] + 1:], self.tolerance)

                indicies2[0] = Line.firstNonZero(self.normalVector.coor, self.tolerance)
                indicies2[1] = Line.firstNonZero(self.normalVector.coor[indicies2[0] + 1:], self.tolerance)

                if indices1 != indices2:
                    raise Exception
                
                A,B = self.normalVector.coor[indicies1[0]], self.normalVector.coor[indicies1[1]] 
                C,D = line.normalVector.coor[indicies2[0]], line.normalVector.coor[indicies2[1]] 
                denom = A * D - B * C
                return Vector([(D * self.constant - B * line.constant) / denom, (-C * self.constant + A * line.constant) / denom])

            except ZeroDivisionError:
                if self.normalVector == line.normalVector:
                    return self.normalVector
                elif self.constant == line.constant:
                    return Vector()
                else:
                    return None
                
            except Exception:
                raise Exception(sys.exc_info()[0])
            
    def __eq__(self, line):
        if not self.normalVector.parallel(line.normalVector):
            return False

        return self.basePoint.subVec(line.basePoint).perp(self.normalVector)

    def firstNonZero(coor, tolerance):
        for index, num in enumerate(coor):
            if abs(num) > 0 + tolerance:
                return index

        raise Exception('No Non-Zero Coefficients')
    
    def __str__(self):
        msg = "{0} + t{1}".format(self.basePoint, self.normalVector)
        return msg

if __name__ == "__main__":
    l1 = Line([1,0], 1)
    l2 = Line([0,3],6)
    print(l1.intersection(l2))
    
