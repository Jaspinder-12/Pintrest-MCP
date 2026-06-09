#day 1
num = 5
if num > 0 :
    print("The number is positive")
elif num < 0 :
    print("the number is negative")
else:
    print("0")

a = 20
b = 50
if a > b:
    print(a, "is greater than", b)
elif a < b:
    print(a, "is less than", b)
else:
    print(a, "is equal to", b)

for i in range(1,7):
    print(i * 8)
    
#Day2 
name = "Jaspinder"
def greet(name):
    print("Hello, " + name)


greet(name)

name = "Jaspinder"
def introduce(name):
    print("My name is", name)

introduce(name)


def multiply_by_5(num):
  print(num * 5)
