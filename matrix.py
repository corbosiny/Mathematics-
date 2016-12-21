class Matrix():

    def __init__(self, matrix):
        self.matrix = matrix                                                #2D array, each element is a row
        self.rows = len(matrix)                                             #so the number of elements is the number of rows
        self.columns = len(matrix[0])                                       #and the length of an element(or row) is the number of columns

        for x in matrix:                                                    #checking if they put in a valid matrix 
            if len(x) != self.columns:
                raise ValueError('All rows must be of the same length')     

    def __add__(self, b):                                                   #edits what happens when two matricies are added
        if b.rows != self.rows or b.columns != self.columns:                #if the matrices are not the same size raise an error
            raise ValueError('Matricies must be of the same size')

        result = Matrix.zero(self.rows, self.columns)                       # creates a zero matrix of the same size
        
        for x in range(self.rows):                                          #sets each value in the matrix equal to the sum of its respective counterparts in the other two matrices
            for y in range(self.columns):
                result.matrix[x][y] = self.matrix[x][y] + b.matrix[x][y]
                
        return result

    def __sub__(self, b):                                                   #edits what happens when two matricies are added
        if b.rows != self.rows or b.columns != self.columns:                #if the matrices are not the same size raise an error
            raise ValueError('Matricies must be of the same size')

        result = Matrix.zero(self.rows, self.columns)                              # creates a zero matrix of the same size
        
        for x in range(self.rows):                                          #sets each value in the matrix equal to the sum of its respective counterparts in the other two matrices
            for y in range(self.columns):
                result.matrix[x][y] = self.matrix[x][y] - b.matrix[x][y]
                
        return result

    def __mul__(self, b):                                                   #edits what happens when two matricies are multiplied
        if self.columns != b.rows:
            raise ValueError('The columns of the first matrix must equal the number of the rows of the second')   #raise error if the matrices are not of the right side

        result = Matrix.zero(self.rows, b.columns)                                         #creates empty matrix of the rows of the first, and the columns of the second

        for x in range(self.rows):                                                  #goes through each row and each column of the empty matrix
            for y in range(b.columns):                               
                for k in range(self.columns):                                       #adds the products of each respective pair from the first's row and the second's column
                    result.matrix[x][y] += self.matrix[x][k] * b.matrix[k][y]

        return result

    def transpose(matrix):                                                  #static, returns the transpose of an input matrix
        result = Matrix.zero(matrix.columns, matrix.rows)                   #makes zero matrix of opposite dimensions
        for x in range(matrix.rows):                                        #goes through every row and column and sets the mirrored spot in the new matrix to that same value
            for y in range(matrix.columns):
                result.matrix[y][x] = matrix.matrix[x][y]
                
        return result
    
    def transpose(self):                                                    #non-static version, returns the transpose of the instinces matrix
        result = Matrix.zero(self.columns, self.rows)                       #look at the first version above for a description
        for x in range(self.rows):                                          
            for y in range(self.columns):
                result.matrix[y][x] = self.matrix[x][y]
                
        return result
    
    def zero(rows, columns):                                                #creates a matrix of zeros of the input dimensions
        matrix = []
        for x in range(rows):                                               #will run through and create each row
            row = []                                                        #initializes an empty list for each row
            for y in range(columns):                                        #will go down the length of each row
                row.append(0)                                               #will fill it up with zeros
            matrix.append(row)                                              #will append that row

        return Matrix(matrix)      

    def identity(dimension):                                                #creates an identity matrix of the input dimensions(must be a square matrix)
        result = Matrix.zero(dimension, dimension)     
        for x in range(dimension):                                          #just goes through each row and puts a one into the index of that row number
            result.matrix[x][x] = 1

        return result

    def __str__(self):                                                      #just prints out every row when you try to print the class
        matrixStr = ''
        for x in range(self.rows):
            matrixStr += str(self.matrix[x])
            matrixStr += '\n'

        return matrixStr
    
if __name__ == "__main__":
    matrix = Matrix([[1,2,3],[1,2,3],[1,2,3]])
    matrix2 = Matrix([[1],[1],[1]])
    print(matrix * matrix2)
