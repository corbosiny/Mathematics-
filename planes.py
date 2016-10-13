from vector import Vector

class Plane(): #deals with lines of the form Ax + By = k, then paramaeritizes them in 3D of the form basepoint + t<direction vector> 

    def __init__(self, normalVector= [0,0,0], constant = 0, tolerance = .01, dp = 3):
        self.normalVector = Vector(normalVector, tolerance, dp)
        self.constant = constant
        
        if constant != 0:
            index = Plane.firstNonZero(normalVector, tolerance)
            basePointCoor = [0] * len(normalVector)
            basePointCoor[index] = round(constant / normalVector[index], dp)
            self.basePoint = Vector(basePointCoor, tolerance, dp)

        else:
            self.basePoint = Vector()
        
        self.tolerance = tolerance
        self.dp = dp
        
    def parallel(self, plane):
        return self.normalVector.parallel(plane.normalVector)

    def perp(self, plane):
        return abs(self.normalVector.dotProduct(plane.normalVector)) <= 0 + self.tolerance

    def intersection(self, plane):
        if self.parallel(plane) and self != plane:
            return None
        elif self == plane:
            return 'INFINITE'

        else:
            try:
                A,B,_ = self.normalVector.coor
                C,D,_ = plane.normalVector.coor
                denom = A * D - B * C
                return Vector([(D * self.constant - B * plane.constant) / denom, (-C * self.constant + A * plane.constant) / denom])
            except ZeroDivisionError:
                if self.normalVector == plane.normalVector:
                    return self.normalVector
                elif self.constant == plane.constant:
                    return Vector()
                else:
                    return None

    def pointDistance(self, point):
        A, B, C = self.normalVector.coor
        D = self.constant

        numer = abs(A * point[0] + B * point[1] + C * point[2])
        denom = (A ** 2 + B ** 2 + C ** 2) ** .5
        return numer / denom
    
    def __eq__(self, plane):
        if not self.normalVector.parallel(plane.normalVector):
            return False

        return self.basePoint.subVec(plane.basePoint).perp(self.normalVector)

    def firstNonZero(coor, tolerance):
        for index, num in enumerate(coor):
            if abs(num) > 0 + tolerance:
                return index

        raise Exception('No Non-Zero Coefficients')
    
    def __str__(self):
        msg = "{0}x + {1}y + {2}z = {3}".format(self.normalVector.coor[0], self.normalVector.coor[1], self.normalVector.coor[2], self.constant)
        return msg

if __name__ == "__main__":
    p1 = Plane([2,3,4], 5)
    p2 = Plane([4,6,8], 11)
    print(p1 == p2)
    print(p1.parallel(p2))
    
