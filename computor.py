import re
import sys
import math

def parse_polynomial(polynomial_str):
    """
    This functions will parse our equations and determine
    the degree of the polynom.
    """
    sides = polynomial_str.split("=")
    if len(sides) != 2:
        print("Invalid equation format. Please provide a valid equation with a single '=' sign.")
        sys.exit(1)
    regex = r"([+-]?\s*\d*\.?\d*)\s*\*\s*X\^(\d+)"
    matches = re.findall(regex, polynomial_str)
    
    left_side_matches = re.findall(regex, sides[0])
    right_side_matches = re.findall(regex, sides[1])

    coefficients = {}
    
    for match in left_side_matches:
        coefficient = float(match[0].replace(" ", "")) if match[0] else 1.0
        exponent = int(match[1])
        coefficients[exponent] = coefficients.get(exponent, 0) + coefficient

    for match in right_side_matches:
        coefficient = float(match[0].replace(" ", "")) if match[0] else 1.0
        exponent = int(match[1])
        coefficients[exponent] = coefficients.get(exponent, 0) - coefficient
    
    return coefficients

def print_reduced_form(coefficients):
    """This function prints the reduced form of our polynom."""
    terms = []
    for exponent, coefficient in sorted(coefficients.items()):
        if exponent == 0:
            terms.append(f"{coefficient} * X^0")
        elif exponent == 1:
            terms.append(f"{coefficient} * X^1")
        else:
            terms.append(f"{coefficient} * X^{exponent}")
    reduced_form = " + ".join(terms)
    print(f"Reduced form: {reduced_form} = 0")

def solve_degree_2(coefficients):
        
    a = coefficients.get(2, 0)
    b = coefficients.get(1, 0)
    c = coefficients.get(0, 0)
    
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        print("Discriminant is strictly positive, the two solutions are:")
        print(round(x1, 6))
        print(round(x2, 6))
    elif discriminant == 0:
        x = -b / (2*a)
        print("Discriminant is zero, the solution is:")
        print(round(x, 6))
    else:
        print("Discriminant is strictly negative, there is no real solution.")

def main():
    if len(sys.argv) != 2:
        print("Usage: ./computor <polynomial>")
        return
    
    polynomial_str = sys.argv[1]
    coefficients = parse_polynomial(polynomial_str)
    
    print_reduced_form(coefficients)
    
    degree = max(coefficients.keys(), default=0)
    print(f"Polynomial degree: {degree}")
    
    if degree == 2:
        solve_degree_2(coefficients)
    elif degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
    else:
        print("Polynomial degree is less than 2, it's not a quadratic equation.")

if __name__ == "__main__":
    main()
