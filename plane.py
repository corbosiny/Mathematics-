from vector import Vector
import matrix

class Plane(): #deals with lines of the form Ax + By = k, then paramaeritizes them in 3D of the form basepoint + t<direction vector> 

    def __init__(self, normalVector= [0,0,0], constant = 0, tolerance = .01, dp = 3): #dp is decimal points
        self.normalVector = Vector(normalVector, tolerance, dp)
        self.constant = constant
        
        self.tolerance = tolerance
        self.dp = dp
        
    def parallel(self, plane):                      #returns if a plance is parallel to it by checking their normal vectors
        return self.normalVector.parallel(plane.normalVector)

    def perp(self, plane):                          #checks if a plane is perpendicular to a plane by checking the normal vectors
        return abs(self.normalVector.dotProduct(plane.normalVector)) <= 0 + self.tolerance

    def intersect(self, plane, plane2):             #finds intersection of three planes
        if self.parallel(plane) and self != plane:
            return None, None

        elif self == plane:
            return None, 'INFINITE SOLUTIONS'
        
        else:
            newMatrix = matrix.Matrix([self.normalVector.coor, plane.normalVector.coor, plane2.normalVector.coor])
            newSolutions = matrix.Matrix([[self.constant],[plane.constant],[plane2.constant]])

            newMatrix, solutions = newMatrix.equationSolver(newSolutions)
            if solutions != 'INFINITE SOLUTIONS' or solutions != "NO SOLUTION":
                return newMatrix, solutions
            elif solutions == 'INFINITE SOLUTIONS':
                return newMatrix, solutions
            else:
                return newMatrix, "NO SOLUTION"
            
    def pointDistance(self, point):     #distance of point to a plane
        A, B, C = self.normalVector.coor
        D = self.constant

        numer = abs(A * point[0] + B * point[1] + C * point[2])
        denom = (A ** 2 + B ** 2 + C ** 2) ** .5
        return numer / denom

    #everything below here just defines mainly how scalar operations work on planes and equality functions
    def __eq__(self, plane):
        num1 = plane.normalVector.coor[0] / self.normalVector.coor[0]
        nums = [x / y for x, y in zip(plane.normalVector.coor, self.normalVector.coor)]
        nums.append(plane.constant / self.constant)
        num2 = sum(nums) / len(nums)
        return num1 == num2

    def __add__(self, b):
        return Plane(self.normalVector.coor, self.constant + b, self.tolerance, self.dp)

    def __sub__(self, b):
        return Plane(self.normalVector.coor, self.constant + b, self.tolerance, self.dp)

    def __mul__(self, b):
        return Plane([x * b for x in self.normalVector.coor], self.constant * b, self.tolerance, self.dp)

    def __truediv__():
        return Plane([x / b for x in self.normalVector.coor], self.constant / b, self.tolerance, self.dp)

    def __floordiv__():
        return Plane([x / b for x in self.normalVector.coor], self.constant / b, self.tolerance, self.dp)
    
    def __iter__(self):
        return self.normalVector.coor
    
    def __getitem__(self, key):
        return self.normalVector.coor[key]
    
    def firstNonZero(coor, tolerance): #returns the first nonzero term in the coordinates
        for index, num in enumerate(coor):
            if abs(num) > 0 + tolerance:
                return index

        raise Exception('No Non-Zero Coefficients')
    
    def __str__(self):
        msg = "{0}x + {1}y + {2}z = {3}".format(self.normalVector.coor[0], self.normalVector.coor[1], self.normalVector.coor[2], self.constant)
        return msg

if __name__ == "__main__":      #just some test code
    p1 = Plane([2,3,4], 5)
    p2 = Plane([1,7,3], 10)
    p3 = Plane([-2,-4,5], 7)
    matrix, solutions = p1.intersect(p2, p3)
    print(matrix)
    print()
    print(solutions)
    
