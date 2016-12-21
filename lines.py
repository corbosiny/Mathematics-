from vector import Vector

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
                newCoor = [0,0,0]
                if self.normalVector.coor.count(0) == 2 and self.normalVector.coor.count(0) == 2:
                    index1 = Line.firstNonZero(self.normalVector.coor, self.tolerance)
                    index2 = Line.firstNonZero(line.normalVector.coor, self.tolerance)

                    if index1 == index2:
                        return None
                    
                    newCoor[index1] = self.constant / self.normalVector.coor[index1]
                    newCoor[index2] = line.constant / line.normalVector.coor[index2]

                elif self.normalVector.coor.count(0) == 2 and line.normalVector.coor[Line.firstNonZero(self.normalVector.coor, self.tolerance)] != 0:
                    index1 = Line.firstNonZero(self.normalVector.coor, self.tolerance)
                    index2 = Line.firstNonZero(line.normalVector.coor, line.tolerance)
                    while index2 == index1:
                        index2 = Line.firstNonZero(line.normalVector.coor, line.tolerance)

                    newCoor[index1] = self.constant / self.normalVector.coor[index1]
                    newCoor[index2] = line.constant - line.normalVector.coor[index1] * newCoor[index1]
                    
                elif line.normalVector.coor.count(0) == 2 and self.normalVector.coor[Line.firstNonZero(line.normalVector.coor, line.tolerance)] != 0:
                    index1 = Line.firstNonZero(line.normalVector.coor, line.tolerance)
                    index2 = Line.firstNonZero(self.normalVector.coor, self.tolerance)
                    while index2 == index1:
                        index2 = Line.firstNonZero(self.normalVector.coor, self.tolerance)

                    newCoor[index1] = line.constant / line.normalVector.coor[index1]
                    newCoor[index2] = self.constant - self.normalVector.coor[index1] * newCoor[index1]
                
                else:
                    raise Exception('Vectors must be in the same plane')    

                return Vector(newCoor)
            
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
    