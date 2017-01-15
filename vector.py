import math

class Vector():
    
    def __init__(self, coor = [], tolerance = .01, decimalPlaces = 3):
        try:
            while len(coor) < 3: #this is to make sure that the cross product is defined
                coor.append(0)

            self.coor = tuple(coor)
            self.tolerance = tolerance
            self.dp = decimalPlaces
            
            for x in coor:
                int(x)
            
        except ValueError:
            raise ValueError('The coordinates must be actual numbers')
    

    def magnitude(self):    #returns vector magnitude
        return sum([x ** 2 for x in self.coor]) ** .5

    def normalize(self): #normalize a vector into its unit vector state
        try:
            mag = self.magnitude()
            return Vector([round(x / mag, self.dp) for x in self.coor])
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot Normalize the Zero Vector') 
            

    def dotProduct(self, vec):
        return sum([round(x * y, self.dp) for x,y in list(zip(self.coor, vec.coor))])

    def angle(self, vec): #angle between vectors
        try:
            return round(math.acos(self.dotProduct(vec) / (self.magnitude() * vec.magnitude())), self.dp)
        except ZeroDivisionError:
            return math.pi/2
        
    def angleD(self, vec):  #angle between vectors in degrees
        return round(math.degrees(self.angle(vec)), self.dp)
        
    def perp(self, vec):    #compares if two vectors are perpendicular
        try:
            dot = self.dotProduct(vec)
            return abs(dot) < self.tolerance
        except ZeroDivisionError:
            return True
            
    def parallel(self, vec):    #compares if two vectors are parallel
        try:
            return self.crossProduct(vec) == Vector()
        except ZeroDivisionError:
            return False
            
    def crossProduct(self, vec):
        try:
            x1, y1, z1 = self.coor
            x2, y2, z2 = vec.coor
            newCoor = [y1 * z2 - y2 * z1, x1 * z2 - x2 * z1, x1 * y2 - x2 * y1]
            return Vector([round(x, self.dp) for x in newCoor])

        except ValueError as e:
            if 'too many values to unpack' in str(e):
                raise Exception('Vector module cross product only defined up to three dimensions')
            
    def comp(self, vec): #scalar component of one vector on another
        try:
            return self.dotProduct(vec.normalize())
        except ZeroDivisionError:
            return 0
        
    def proj(self, vec): #vector projection of one vector on another
        try:
            return vec.normalize().scalar(self.comp(vec))
        except ZeroDivisionError:
            return Vector()

    #everything below here just defines mainly how scalar operations work on planes and equality functions
    def __eq__(self, vec):
        return self.coor == vec.coor

    def __mul__(self, scal):
        return Vector([round(x * scal, self.dp) for x in self.coor])

    def __floordiv__(self, scal):
        return Vector([round(x / scal, self.dp) for x in self.coor])
        
    def __truediv__(self, scal):
        return Vector([round(x / scal, self.dp) for x in self.coor])

    def __add__(self, vec):
        if isinstance(vec, Vector):
            while len(self.coor) < len(vec.coor):
                self.coor.append(0)
            while len(vec.coor) < len(self.coor):
                vec.coor.append(0)
                    
            return Vector([x + y for x,y in zip(self.coor, vec.coor)], self.tolerance, self.dp)

        raise ValueError("Unsupported operands between Vector and type %s" % type(vec))

    def __sub__(self, vec):
        if isinstance(vec, Vector):
            while len(self.coor) < len(vec.coor):
                self.coor.append(0)
            while len(vec.coor) < len(self.coor):
                vec.coor.append(0)
                    
            return Vector([x - y for x,y in zip(self.coor, vec.coor)], self.tolerance, self.dp)

    def __value__(self):
        return self.coor

    def __iter__(self):
        return self.coor    
    
    def __getitem__(self, key):
        return self.coor[key]
        
    def __str__(self):
        output = "<"
        for x in self.coor:
            output += str(x) + ','
        output = output.strip(',')
        output += '>'
        return output


if __name__ == "__main__":
    vector1 = Vector([2,0])
    vector2 = Vector([-.5,0,2])
    
    print(vector1 - vector2)
