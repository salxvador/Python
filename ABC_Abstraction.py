
from abc import ABC, abstractmethod


##Your class should contain at least one abstract method and one regular method.  
##Create a child class that defines the implementation of its parents abstract method.
##Create an object that utilizes both the parent and child methods.
##Add comments throughout your Python explaining your code.

##This is a test
##Parent abstract Class:
class Animal(ABC):
    #regular method move():
    def move(self):
        print("I am crawling around.")

    #abstract method speak() requires decorator '@abstractmethod'
    @abstractmethod
    def speak(self):
        pass

##Child Class:
class Dog(Animal):
    #must define abstract method that we passed on in the parent:
    def speak(self):
        print("I can bark and growl.")

#instantiate object of child class:
spot = Dog()
#call the regular method defined in parent:
spot.move()
#call the abstract method only defined in child class:
spot.speak()
 
