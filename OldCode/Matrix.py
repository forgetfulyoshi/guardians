from math import *

class Matrix():
    def __init__(self, vector1, vector2, vector3):
        assert(len(vector1) == 3)
        assert(len(vector2) == 3)
        assert(len(vector3) == 3)
        
        self.matrix = [vector1, vector2, vector3]
        # NOTE: THESE ARE COLUMN VECTORS!!

    def __getitem__(self, value):
        
        return self.matrix[value]
    
    def __mul__(self, matrix2):
                   
        newMatrix = []
        
        newMatrix.append( [  self.matrix[0][0] * matrix2[0][0] + self.matrix[0][1] * matrix2[1][0] + self.matrix[0][2] * matrix2[2][0],
                             self.matrix[1][0] * matrix2[0][0] + self.matrix[1][1] * matrix2[1][0] + self.matrix[1][2] * matrix2[2][0],
                             self.matrix[2][0] * matrix2[0][0] + self.matrix[2][1] * matrix2[1][0] + self.matrix[2][2] * matrix2[2][0] ])
        
        newMatrix.append( [  self.matrix[0][0] * matrix2[0][1] + self.matrix[0][1] * matrix2[1][1] + self.matrix[0][2] * matrix2[2][1],
                             self.matrix[1][0] * matrix2[0][1] + self.matrix[1][1] * matrix2[1][1] + self.matrix[1][2] * matrix2[2][1],
                             self.matrix[2][0] * matrix2[0][1] + self.matrix[2][1] * matrix2[1][1] + self.matrix[2][2] * matrix2[2][1] ])
        
        newMatrix.append( [  self.matrix[0][0] * matrix2[0][2] + self.matrix[0][1] * matrix2[1][2] + self.matrix[0][2] * matrix2[2][2],
                             self.matrix[1][0] * matrix2[0][2] + self.matrix[1][1] * matrix2[1][2] + self.matrix[1][2] * matrix2[2][2],
                             self.matrix[2][0] * matrix2[0][2] + self.matrix[2][1] * matrix2[1][2] + self.matrix[2][2] * matrix2[2][2] ])
        return newMatrix
    
    
# 					        a b c
#In general, the inverse matrix of a 3X3 matrix d e f
#					        g h i
#is 
#
#	    1                       (ei-fh)   (ch-bi)   (bf-ce)
#-----------------------------   x   (fg-di)   (ai-cg)   (cd-af)
#a(ei-fh) - b(di-fg) + c(dh-eg)      (dh-eg)   (bg-ah)   (ae-bd)

    def inverse(self):
        inverseMatrix = []
        a = self.matrix[0][0]
        b = self.matrix[1][0]
        c = self.matrix[2][0]
        d = self.matrix[0][1]
        e = self.matrix[1][1]
        f = self.matrix[2][1]
        g = self.matrix[0][2]
        h = self.matrix[1][2]
        i = self.matrix[2][2]
        
        determinant = 1 / ( (a*(e*i-f*h)) - (b*(d*i-f*g)) + (c*(d*h-e*g)))
            
        column1 = [e*i-f*h,
                   f*g-d*i,
                   d*h-e*g]
        inverseMatrix.append(column1)
        column2 = [c*h-b*i,
                   a*i-c*g,
                   b*g-a*h]
        inverseMatrix.append(column2)
        column3 = [b*f-c*e,
                   c*d-a*f,
                   a*e-b*d]
        inverseMatrix.append(column3)
        
        for x in inverseMatrix:
            for y in x:
                y = y*determinant
                
        return inverseMatrix
    
def changeHeadingMatrix(heading):
    headingMatrix = Matrix([cos(radians(heading)), sin(radians(heading)), 0],
                           [-sin(radians(heading)), cos(radians(heading)), 0],
                           [0,0,1])
    return headingMatrix
    
def changePitchMatrix(pitch):
    pitchMatrix = Matrix([1,0,0],
                         [0, cos(radians(pitch)), sin(radians(pitch))],
                         [0, -sin(radians(pitch)), cos(radians(pitch))])
    return pitchMatrix
    
def changeRollMatrix(roll):
    rollMatrix = Matrix([cos(radians(roll)), 0, sin(radians(roll))],
                        [0,1,0],
                        [-sin(radians(roll)), 0, cos(radians(roll))])
                        
    return rollMatrix
        