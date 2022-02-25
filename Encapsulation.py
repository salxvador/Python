##This class should make use of a private attribute or function.
##This class should make use of a protected attribute or function.
##Create an object that makes use of protected and private.
##Add comments throughout your Python explaining your code.

#define class
class Practice:
    def __init__(self):
        self._protectedNum = 99 #protected var
        self.__privateNum = 88  #private var

    # Will need this method to retrieve private value
    def getPrivate(self):
        print(self.__privateNum)

#instantiate
obj = Practice()

# Protected var can be accessed (printed) regularly
print(obj._protectedNum)

## print(obj.__privateNum)
"""
    above print statement throws error:
    AttributeError: 'Practice' object has no attribute '__privateNum'
    because it is not retrievable outside fo the class methods.
"""

## must use defined method to retrieve __private value
obj.getPrivate()
