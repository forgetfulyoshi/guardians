from Matrix import *

matrix1 = Matrix( [1,0,0], [0,1,0], [0,0,1] )

matrix2 = Matrix( [1,2,3], [3,5,7], [9,2,13] )
                
##testMatrix = matrix1 * matrix2

matrix = changeRollMatrix(5)

for i in range(3):
    print matrix[i]
    