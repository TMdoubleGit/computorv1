import re
import sys
import math

def is_valid_exponent(exponent):
    """This function checks if all exponents are comprised between 0 and 2."""
    try:
        float(exponent)
        if exponent != int(exponent) or exponent < 0 or exponent > 2:
            return False
        return True
    except ValueError:
        return False

def is_valid_expression(expression, regex):
    """This function checks if all components of the polynomial sent as argument resclapects the format we use as regex."""
    elements = re.split(r'\s*[\+\-]\s*', expression)
    for element in elements:
        element = element.strip()
        if not re.fullmatch(regex, element):
            return False
    return True

def parse_polynomial(polynomial_str):
    """This functions will parse our equations and determine the degree of the polynomial."""
    sides = polynomial_str.split("=")
    if len(sides) != 2:
        print("Invalid equation format. Please provide a valid equation with a single '=' sign.")
        sys.exit(1)
    regex = r"([+-]?\s*\d*\.?\d*)\s*\*\s*X\^([+-]?\d+(?:\.\d+)?)"

    for side in sides:
        side = side.strip()
        if (is_valid_expression(side, regex) == False and len(side) > 1 ):
            print("Invalid equation format. All polynomial should be written 'a * x^b' with 'a' belonging to real numbers and 'b' an int from 0 to 2")
            sys.exit(1)

    left_side_matches = re.findall(regex, sides[0])
    right_side_matches = re.findall(regex, sides[1])

    coefficients = {}
    
    for match in left_side_matches:
        coefficient = float(match[0].replace(" ", "")) if match[0] else 1.0
        exponent = float(match[1]) if match[1] else 1.0
        if not is_valid_exponent(exponent):
            print("Invalid equation format. All polynomial should be written 'a * x^b' with 'a' belonging to real numbers and 'b' an int from 0 to 2")
            sys.exit(1)
        coefficients[exponent] = coefficients.get(exponent, 0) + coefficient

    for match in right_side_matches:
        coefficient = float(match[0].replace(" ", "")) if match[0] else 1.0
        exponent = float(match[1]) if match[1] else 1.0
        if not is_valid_exponent(exponent):
            print("Invalid equation format. All polynomial should be written 'a * x^b' with 'a' belonging to real numbers and 'b' an int from 0 to 2")
            sys.exit(1)
        coefficients[exponent] = coefficients.get(exponent, 0) - coefficient

    return coefficients

def print_reduced_form(coefficients):
    """This function prints the reduced form of our polynom."""
    terms = []
    for exponent, coefficient in sorted(coefficients.items()):
        if exponent == 0 and int(coefficient) != 0:
            terms.append(f"{coefficient} * X^0")
        elif exponent == 1 and int(coefficient) != 0:
            terms.append(f"{coefficient} * X^1")
        elif exponent == 2 and int(coefficient) != 0:
            terms.append(f"{coefficient} * X^{int(exponent)}")
    reduced_form = " + ".join(terms)
    print(f"Reduced form: {reduced_form} = 0")

def solve_degree_1(coefficients):
    """This function aims to solve polynomial of degree 1."""
    b = coefficients.get(1, 0)
    c = coefficients.get(0, 0)

    x = -c / b
    print("The solution is:")
    print(round(x, 6))

def solve_degree_2(coefficients):
    """This function aims to solve polynomial of degree 2."""
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
        print("Discriminant is strictly negative, the two solutions are:")
        if 2*a != 1:
            print(f"({-b} + i * √{- discriminant}) / {2*a}")
            print(f"({-b} - i * √{- discriminant}) / {2*a}")
        else:
            print(f"{-b} + i * √{- discriminant}")
            print(f"{-b} - i * √{- discriminant}")

def main():
    if len(sys.argv) != 2:
        print("Usage: ./computor <polynomial>")
        return
    
    polynomial_str = sys.argv[1]
    coefficients = parse_polynomial(polynomial_str)
    if coefficients == {}:
        sys.exit(1)
    
    degree_tbc = max(coefficients.keys(), default=0)
    if float(coefficients.get(2, 0)) != 0:
        degree = 2
    elif float(coefficients.get(1, 0)) != 0:
        degree = 1
    elif float(coefficients.get(0, 0)) != 0:
        degree = 0
    elif degree_tbc > 2:
        degree = degree_tbc
        pass
    
    if degree == 1:
        print_reduced_form(coefficients)
        print(f"Polynomial degree: {int(degree)}")
        solve_degree_1(coefficients)
    elif degree == 2:
        print_reduced_form(coefficients)
        print(f"Polynomial degree: {int(degree)}")
        solve_degree_2(coefficients)
    elif degree > 2:
        print_reduced_form(coefficients)
        print(f"Polynomial degree: {int(degree)}")
        print("The polynomial degree is strictly greater than 2, I can't solve.")
    else:
        print(degree)
        print("This is an exception, all real numbers are a solution!")
        print("try again with a proper polynomial!")

if __name__ == "__main__":
    main()
