# Python Program to find the L.C.M. of two input number

# define a function

# GCD and LCM are not in math module.  They are in gmpy, but these are simple enough:

def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)

# change the values of num1 and num2 for a different result
num1 = 115792089237316195423570985008687907853269984665640564039457584007913129639937
num2 = 1000000000000000000000000000000000000

# uncomment the following lines to take input from the user
#num1 = int(input("Enter first number: "))
#num2 = int(input("Enter second number: "))

print("The L.C.M. of", num1, "and", num2, "is", lcm(num1, num2))
