# This is a comment

'''
This is a block comment

you can enter multiple lines

and it is not interpreted
'''
"""
This is also a block comment

See?
"""
'''
# Print Hello World
x = "Hello World"
print(x)

# User Input
x = raw_input("Enter a number: ")
x = int(x)


# If statement
if x > 10:
    print("{} is greater than 10".format(x))
elif x ==10:
    print("{} is 10".format(x))
else:
    print("%s is less than 10" % x)

# While statement
while x > 10:
    x = int(raw_input("Enter a number less than 10: "))


# For statement
for x in range(0, x):
    if x % 2 == 0:
        print(x)

# Function

def divideBy2(x, divisionNumber=2):
    """ All functions should have a header describing the function

    INPUT
    x [ number ] - number to be divided

    RETURNS
    [ number ] - divides the input by 2
    """
    y = x/divisionNumber
    return(y)

divVal = divideBy2(x, 3)
print("{} is half of {}".format(divVal, x))

print(9/2)
print(9/2.0)
print(9/2.)

'''
### CHALLENGE - have user enter a number and calculate
#               all the factors
in_x = raw_input("Enter a number: ")
in_x = int(in_x)

for x in range(1, in_x):
    if in_x % x == 0:
        print(x)


        
