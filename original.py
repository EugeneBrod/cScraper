import numpy as np

# WRITTEN BY: EUGENE BRODSKY
# GUID: a62af8a7-c93b-44f2-aeea-fa1901b4ee0a

class Engine():

    def __init__(self, array):
        self.array = array
        self.newArray = array
    

    def transformAndReMapInput(self, inputString, transformString):

        self.newArray = np.copy(self.array)
        indiciesOfInput = self.getIndiciesofString(inputString)
        self.parseStringAndTransformMatrix(transformString)
        outputString = self.gatherRemappedKeys(indiciesOfInput)
        self.logChanges(inputString, outputString, transformString)


    # Assuming every character of the input matrix is unique, otherwise remapping the input string
    # is an ill-formed problem.
    def getIndiciesofString(self, inputString):

        res = []
        for c in inputString:
            for i, row in enumerate(self.array):
                for j, val in enumerate(row):
                    if val == c:
                        res.append((i,j))
        return res


    def parseStringAndTransformMatrix(self, transformString):

        transformations = self.parseTransformString(transformString)
        self.transformMatrix(transformations)
        

    def transformMatrix(self, transformations):

        for i in transformations:
            

            tranformIdentier = i[0]
            if tranformIdentier == 'S':
                self.shiftMatrix(i)
            if tranformIdentier == 'V':
                self.flipMatrixVertically()
            if tranformIdentier == 'H':
                self.flipMatrixHorizontally()



    def shiftMatrix(self, transformation):

        shiftString = transformation[1:]
        if shiftString[0] == '-':
            shiftAmmount = - int(shiftString[1:])
        else:
            shiftAmmount = int(shiftString[0:])

        for i, arr in enumerate(self.newArray):
            self.newArray[i] = np.roll(self.newArray[i], shiftAmmount)


    def flipMatrixVertically(self):

        self.newArray = np.flipud(self.newArray)


    def flipMatrixHorizontally(self):

        self.newArray = np.fliplr(self.newArray)


    # Need to learn how to use regular expressions, for now, this will have to do.
    def parseTransformString(self, transformString):

        res = []
        inShift = False
        singleTransform = ""

        for i in transformString:
            if inShift:
                if i == 'H' or i == 'V':
                    inShift = False
                    res.append(singleTransform)
                    singleTransform = i
                    res.append(singleTransform)
                    singleTransform = ""
                    continue
                if i == 'S':
                    res.append(singleTransform)
                    singleTransform = i
                    continue
                if i == '-' or i.isdigit():
                    singleTransform += i
                    continue

            if not inShift:
                singleTransform += i
                if i == 'S':
                    inShift = True
                    continue
                res.append(singleTransform)
                singleTransform = ""
        if len(singleTransform) != 0:
            res.append(singleTransform)
            
        return res


    def gatherRemappedKeys(self, indicies):

        res = ""
        for i in indicies:
            res += self.newArray[i[0],i[1]]
        return res


    def logChanges(self,inputString, outputString, transfromation):
        
        print("Hello Beyond12!\n")
        print("Here is the keyboard before the transformation.\n")
        print("________________________________________________\n")
        print(self.array)
        print("\n")
        print("________________________________________________\n")
        print("\n")
        print("After applying the following transformation => " + transfromation + ", the keyboard looks like this! \n")
        print("________________________________________________\n")
        print(self.newArray)
        print("\n")
        print("________________________________________________\n")
        print("\n")
        print("If you had typed => " + inputString + " on the original keyboard, the same keys would make to => " + outputString + " on the transformed keyboard!.\n")
        print("\n\n Thank you for the assessement Beyond12!")


# DRIVER


# Setup keyboard array.

row1 = list("1234567890".upper())
row2 = list("qwertyuiop".upper())
row3 = list("asdfghjkl;".upper())
row4 = list("zxcvbnm,./".upper())
keyboard = np.array([row1, row2, row3, row4])

# Inputs

transformString = ["S3H", "V", "H", "S-1", "S-100", "VH", "VHS-1", "S-1V"]
inputString = "HORSE"

# Engine
engine = Engine(keyboard)

for i in transformString:
    engine.transformAndReMapInput(inputString, i)

