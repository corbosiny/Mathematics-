from __future__ import division
import math
from math import sqrt
from operator import *
class Matrix():

    def __init__(self, matrix):
        self.matrix = matrix                                                #2D array, each element is a row
        self.rows = len(matrix)                                             #so the number of elements is the number of rows
        self.columns = len(matrix[0])                                       #and the length of an element(or row) is the number of columns

        for x in matrix:                                                    #checking if they put in a valid matrix 
            if len(x) != self.columns:
                raise ValueError('All rows must be of the same length')     

    def __add__(self, b):                                                   #edits what happens when two matricies are added
        if isinstance(b, Matrix):
            if b.rows != self.rows or b.columns != self.columns:                #if the matrices are not the same size raise an error
                raise ValueError('Matricies must be of the same size')

            result = Matrix.zero(self.rows, self.columns)                       # creates a zero matrix of the same size
            
            for x in range(self.rows):                                          #sets each value in the matrix equal to the sum of its respective counterparts in the other two matrices
                for y in range(self.columns):
                    result.matrix[x][y] = self.matrix[x][y] + b.matrix[x][y]
        else:
            raise ValueError('Unsupported operands for + between type Matrix and type %s' % type(b))
        
        return result

    def __sub__(self, b):                                                   #edits what happens when two matricies are added
        if isinstance(b, Matrix):
            if b.rows != self.rows or b.columns != self.columns:                #if the matrices are not the same size raise an error
                raise ValueError('Matricies must be of the same size')

            result = Matrix.zero(self.rows, self.columns)                              # creates a zero matrix of the same size
            
            for x in range(self.rows):                                          #sets each value in the matrix equal to the sum of its respective counterparts in the other two matrices
                for y in range(self.columns):
                    result.matrix[x][y] = self.matrix[x][y] - b.matrix[x][y]
        else:
            raise ValueError('Unsupported operands for - between type Matrix and type %s' % type(b))
        
        return result

    def __mul__(self, b):                                                   #edits what happens when two matricies are multiplied
        if isinstance(b, Matrix):
            if self.columns != b.rows:
                raise ValueError('The columns of the first matrix must equal the number of the rows of the second')   #raise error if the matrices are not of the right side

            result = Matrix.zero(self.rows, b.columns)                                         #creates empty matrix of the rows of the first, and the columns of the second

            for x in range(self.rows):                                                  #goes through each row and each column of the empty matrix
                for y in range(b.columns):                               
                    for k in range(self.columns):                                       #adds the products of each respective pair from the first's row and the second's column
                        result.matrix[x][y] += self.matrix[x][k] * b.matrix[k][y]
        elif isinstance(b, int):
            result = Matrix.zero(self.rows, self.columns)
            for x in range(self.rows):
                for y in range(self.columns):
                    result.matrix[x][y] = self.matrix[x][y] * b
        else:
            raise ValueError('Unsupported operands for * between type Matrix and type %s' % type(b))
        
        return result

    def __truediv__(self, b):
        if isinstance(b, Matrix):
            result = self * b.inverse()

        elif isinstance(b, int):
            result = Matrix.zero(self.rows, self.columns)
            for x in range(self.rows):
                for y in range(self.columns):
                    result.matrix[x][y] = self.matrix[x][y] / b
    
        else:
            raise ValueError('Unsupported operands for / between type Matrix and type %s' % type(b))

        return result

    def __floordiv__(self, b):
        pass

    def __getitem__(self, i):
        return self.matrix[i]
    
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
        if rows < 1 or columns < 1:
            raise ValueError('Invalid Dimensions, must be greater than zero')
        matrix = []
        for x in range(rows):                                               #will run through and create each row
            row = []                                                        #initializes an empty list for each row
            for y in range(columns):                                        #will go down the length of each row
                row.append(0)                                               #will fill it up with zeros
            matrix.append(row)                                              #will append that row

        return Matrix(matrix)      

    def identity(dimension):                                                #creates an identity matrix of the input dimensions(must be a square matrix)
        if dimension < 1:
            raise ValueError('Invalid Dimensions, must be greater than zero')
        result = Matrix.zero(dimension, dimension)     
        for x in range(dimension):                                          #just goes through each row and puts a one into the index of that row number
            result.matrix[x][x] = 1

        return result

    def Cholesky(self, ztol=1.0e-5):
        # Computes the upper triangular Cholesky factorization of
        # a positive definite matrix.
        res = Matrix([[]])
        res = Matrix.zero(self.rows, self.columns)

        for i in range(self.rows):
            S = sum([(res.matrix[k][i])**2 for k in range(i)])
            d = self.matrix[i][i] - S
            if abs(d) < ztol:
                res.matrix[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError("Matrix not positive-definite")
                res.matrix[i][i] = sqrt(d)
            for j in range(i+1, self.rows):
                S = sum([res.matrix[k][i] * res.matrix[k][j] for k in range(self.rows)])
                if abs(S) < ztol:
                    S = 0.0
                res.matrix[i][j] = (self.matrix[i][j] - S)/res.matrix[i][i]
        return res
    
    def CholeskyInverse(self):
        # Computes inverse of matrix given its Cholesky upper Triangular
        # decomposition of matrix.
        res = Matrix([[]])
        res = Matrix.zero(self.rows, self.columns)
        
        # Backward step for inverse.
        for j in reversed(range(self.rows)):
            tjj = self.matrix[j][j]
            S = sum([self.matrix[j][k]*res.matrix[j][k] for k in range(j+1, self.rows)])
            res.matrix[j][j] = 1.0/tjj**2 - S/tjj
            for i in reversed(range(j)):
                res.matrix[j][i] = res.matrix[i][j] = -sum([self.matrix[i][k]*res.matrix[k][j] for k in range(i+1, self.rows)])/self.matrix[i][i]
        return res
    

    def inverse(self):
        aux = self.Cholesky()
        result = aux.CholeskyInverse()
        return result

    def apply(self, opcode, operand = None):
        result = Matrix.zero(self.rows, self.columns)
        for x in range(self.rows):
            for y in range(self.columns):
                if operand:
                    result.matrix[x][y] = opcode(self.matrix[x][y], operand)
                else:
                    result.matrix[x][y] = opcode(self.matrix[x][y])
                    
        return result

    def applyRow(self, rowNum, opcode, operand = None):
        result = self.makeCopy()
        for y in range(self.columns):
            if isinstance(operand, list):
                result.matrix[rowNum][y] = opcode(self.matrix[rowNum][y], operand[y])
            elif operand:
                result.matrix[rowNum][y] = opcode(self.matrix[rowNum][y], operand)
            else:
                result.matrix[rowNum][y] = opcode(self.matrix[rowNum][y])
                
        return result

    def applyRows(self, rowNums, opcode, operand = None):
        result = self.makeCopy()
        for index, rowNum in enumerate(rowNums):
            for y in range(self.columns):
                if isinstance(operand, list):
                    result.matrix[rowNum][y] = opcode(self.matrix[rowNum][y], operand[index])
                elif operand:
                    result.matrix[rowNum][y] = opcode(self.matrix[rowNum][y], operand)
                else:
                    result.matrix[rowNum][y] = opcode(self.matrix[rowNum][y])
            
        return result

    def applyRowOps(self, rowNums, opcodes, operands = None):
        result = self.makeCopy()
        for index, rowNum in enumerate(rowNums):
            for y in range(self.columns):
                if isinstance(operands, list):
                    result.matrix[rowNum][y] = opcodes[index](self.matrix[rowNum][y], operands[index])
                elif operands:
                    result.matrix[rowNum][y] = opcodes[index](self.matrix[rowNum][y], operands)
                else:
                    result.matrix[rowNum][y] = opcodes[index](self.matrix[rowNum][y])
                    
        return result
    
    def applyColumn(self, columnNum, opcode, operand = None):
        result = self.makeCopy()

        for x in range(self.rows):
            if isinstance(operand, list):
                result.matrix[x][columnNum] = opcode(self.matrix[x][columnNum], operand[x])
            elif operand:
                result.matrix[x][columnNum] = opcode(self.matrix[x][columnNum], operand)
            else:
                result.matrix[x][columnNum] = opcode(self.matrix[x][columnNum])
                
        return result

    def applyColumns(self, columnNums, opcode, operand = None):
        result = self.makeCopy()

        for index, columnNum in enumerate(columnNums):
            for x in range(self.rows):
                if isinstance(operand, list):
                    result.matrix[x][columnNum] = opcode(self.matrix[x][columnNum], operand[index])
                elif operand:
                    result.matrix[x][columnNum] = opcode(self.matrix[x][columnNum], operand)
                else:
                    result.matrix[x][columnNum] = opcode(self.matrix[x][columnNum])

        return result

    def applyColumnOps(self, columnNums, opcodes, operand = None):
        result = self.makeCopy()

        for index, columnNum in enumerate(columnNums):
            for x in range(self.rows):
                if isinstance(operand, list):
                    result.matrix[x][columnNum] = opcodes[index](self.matrix[x][columnNum], operand[index])
                elif operand:
                    result.matrix[x][columnNum] = opcodes[index](self.matrix[x][columnNum], operand)
                else:
                    result.matrix[x][columnNum] = opcodes[index](self.matrix[x][columnNum])

        return result
    
    def swapRows(self, row1, row2):
        result = self.makeCopy()
        temp = result.matrix[row1]
        result.matrix[row1] = result.matrix[row2]
        result.matrix[row2] = temp
        
        return result
        
    def swapColumns(self, column1, column2):
        result = self.makeCopy()
        if column1 - column2 == 0:
            return result
        
        else:
            for x in range(self.rows):
                temp = result.matrix[x][column1]
                result.matrix[x][column1] = result.matrix[x][column2]
                result.matrix[x][column2] = temp
                
        return result


    def rowOp(self, row1, row2, opcode, rowSave = 0):                                            #its always row2 acting on row1, Ex: for sub its row1 - row2
        result = self.makeCopy()

        if rowSave > 1:
            raise ValueError('rowSave flag  must only be set to zero and one')
        for y in range(self.columns):
            result.matrix[row1 * (1 - rowSave) + row2 * rowSave][y] = opcode(result.matrix[row1][y], result.matrix[row2][y])

        return result
    
    def makeCopy(self):
        result = Matrix.zero(self.rows, self.columns)
        for x in range(self.rows):
            for y in range(self.columns):
                result.matrix[x][y] = self.matrix[x][y]
                
        return result

    def determinant(self, row = None, matrix = None):
        if matrix != None:
            if matrix.rows != matrix.columns:
                raise ValueError('Matrix must be a square matrix to calculate the determinant')
            elif matrix.rows == 2:
                return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
            else:
                total = 0
                for y in range(matrix.columns):
                    if matrix[row][y] == 0:
                        continue
                    newRows = []
                    for x in range(matrix.rows):
                        if row == x:
                            continue
                        newRow = []
                        for z in range(matrix.columns):
                            if z == y:
                                continue
                            else:
                                newRow.append(matrix[x][z])
                        newRows.append(newRow)
                    newMatrix = Matrix(newRows)
                    total += matrix[row][y] * self.determinant(row, newMatrix) * int(math.pow(-1, y))
                return total
            
        if self.rows != self.columns:
            raise ValueError('Matrix must be a square matrix to calculate the determinant')
        elif self.rows == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[1][0] * self.matrix[0][1]
        else:
            total = 0
            if row == None:
                row = 0
            for y in range(self.columns):
                if self.matrix[row][y] == 0:
                    continue
                newRows = []
                for x in range(self.rows):
                    if row == x:
                        continue
                    newRow = []
                    for z in range(self.columns):
                        if z == y:
                            continue
                        else:
                            newRow.append(self.matrix[x][z])
                    print(newRow)
                    newRows.append(newRow)
                #print()
                newMatrix = Matrix(newRows)
                #print("New Matrix: ")
                #print(newMatrix)
                total += self.matrix[row][y] * self.determinant(row, newMatrix) * int(math.pow(-1, y))
                #print("Coefficient: ", self.matrix[row][y])
                #print("Partial Determinant: ", self.determinant(row, newMatrix))
                #print("Sign: ", int(math.pow(-1, y)))
                #print("Total: ", total)
                print()
            return total

    def equationSolver(self, solutionsMatrix):
        if self.rows != solutionsMatrix.rows:
            raise ValueError("Must be as many solutions as there are equations(Matrix must have equal rows as the solutions matrix)")
        newMatrix = self.makeCopy()
        newSolutions = solutionsMatrix.makeCopy()

        for y in range(newMatrix.columns):
            allZeroes = True
            print(y)
            if newMatrix[y][y] == 0:
                for x in range(1 + y, newMatrix.rows):
                    if newMatrix[x][y] != 0:
                        allZeroes = False
                        print()
                        print('swapping rows: ', y, x)
                        print("Preswap: ")
                        print(newMatrix)
                        print()
                        newMatrix = newMatrix.swapRows(y, x)
                        newSolutions = newSolutions.swapRows(y, x)
                        print("Post Swap: ")
                        print(newMatrix)
                        print()
                        break;
            else:
                allZeroes = False
                
            if allZeroes:
                print('allzeroes')
                continue
            
            for x in range(1 + y, newMatrix.rows):
                if newMatrix[x][y] != 0:
                    print('eliminating rows: ', x, y)
                    print('pre elimination: ')
                    print(newMatrix)
                    alpha = newMatrix[x][y] / newMatrix[y][y]
                    newMatrix = newMatrix.applyRow(y, mul, alpha)
                    newSolutions = newSolutions.applyRow(y, mul, alpha)
                    print('post applying gamma:')
                    print(newMatrix)
                    newMatrix = newMatrix.rowOp(x,y,sub,0)
                    newSolutions = newSolutions.rowOp(x, y, sub, 0)
                    print('post elimination: ')
                    print(newMatrix)
                    print('unapplying gamma: ')
                    newMatrix = newMatrix.applyRow(y, mul, 1 / alpha)
                    newSolutions = newSolutions.applyRow(y, mul, 1 / alpha)
                    print(newMatrix)
                    print('New solutions: ')
                    print(newSolutions)
                    print()

        #check for no solutions
        for x in range(newMatrix.rows):
            allZeroes = True
            for y in range(newMatrix.columns):
                if not Matrix.isZero(newMatrix[x][y]):
                    allZeroes = False
                    break;
            if allZeroes and not Matrix.isZero(newSolutions[x][0]):
                return newMatrix, 'NO SOLUTION'
            elif allZeroes and Matrix.isZero(newSolutions[x][0]):                                              #infinite solutions, add in paramtertization
                return newMatrix, 'INFINITE SOLUTIONS'
                #parameteritize solution
            
        #solve solutions
        for x in range(newMatrix.rows - 1, -1, -1):
            print("Row:", x)
            y = 0
            while newMatrix[x][y] == 0:
                y += 1
                print("First non-zero term:", y)
            if y != newMatrix.columns - 1:
                k = y + 1
                while k < newMatrix.columns:
                    print('K =', k)
                    print("Prev solution =", newSolutions[x][0])
                    print("Subtracting over:", newMatrix[x][k])
                    newSolutions[x][0] -= newMatrix[x][k]
                    newMatrix[x][k] = 0
                    print("New solution =", newSolutions[x][0])
                    k += 1
            else:
                print(y,"is the final member of the array")
            print('Turning coefficient to one:')
            num = newMatrix[x][y]
            newMatrix = newMatrix.applyRow(x, truediv, num)
            newSolutions = newSolutions.applyRow(x, truediv, num)
            print(newMatrix)
            print("Final solution: ", newSolutions[x][0])
            for z in range(newMatrix.rows):
                newMatrix[z][y] = newSolutions[x][0] * newMatrix[z][y]
            print("Post subsituting %d into the matrix: " % newSolutions[x][0])
            print(newMatrix)
                
        return newMatrix, newSolutions

    def isZero(x):
        return abs(x) < (0 + .001) 
    
    def __eq__(self, b):
        if not isinstance(b, Matrix):
            return False
        else:
            return self.matrix == b.matrix
    
    def __str__(self):                                                      #just prints out every row when you try to print the class
        matrixStr = ''
        for x in range(self.rows):
            matrixStr += '['
            for y in range(self.columns):
                num = self.matrix[x][y]
                if round(num) - num != 0:
                    matrixStr += ("%.2f" % float(self.matrix[x][y]))
                else:
                    matrixStr += str(int(num))
                if (y < self.columns - 1):
                    matrixStr += ', '
            matrixStr += ']'
            if(x < self.rows - 1):
                matrixStr += '\n'
        
        return matrixStr

    def __value__(self):
        return self.matrix
    
if __name__ == "__main__":
    matrix = Matrix([[1,2,1], [-1,1, 2], [1,1,-1]])
    matrix2 = Matrix([[1,-1,2, 5], [2, 3,4,2], [7,4,1,3], [2,9,5,4]])
    matrix3 = matrix2.transpose()
    solutions = Matrix([[7],[5], [1]])
    newMatrix, solutions = matrix.equationSolver(solutions)
    print(newMatrix)
    print()
    print(solutions)
    
