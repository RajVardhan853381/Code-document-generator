"""
Calculator Module - Sample Python File for Testing
Demonstrates various Python features for documentation generation.
"""

from typing import Union, List


class Calculator:
    """A simple calculator class with basic arithmetic operations.
    
    This calculator supports addition, subtraction, multiplication,
    division, and power operations.
    """
    
    def __init__(self, precision: int = 2):
        """Initialize calculator with specified precision.
        
        Args:
            precision: Number of decimal places for results (default: 2)
        """
        self.precision = precision
        self.history: List[str] = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
            
        Examples:
            >>> calc = Calculator()
            >>> calc.add(5, 3)
            8.0
        """
        result = round(a + b, self.precision)
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract second number from first.
        
        Args:
            a: Number to subtract from
            b: Number to subtract
            
        Returns:
            Difference of a and b
        """
        result = round(a - b, self.precision)
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        result = round(a * b, self.precision)
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> Union[float, str]:
        """Divide first number by second.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            Quotient of a and b, or error message if b is zero
            
        Raises:
            ValueError: If divisor is zero
        """
        if b == 0:
            return "Error: Division by zero"
        
        result = round(a / b, self.precision)
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent.
        
        Args:
            base: Base number
            exponent: Exponent value
            
        Returns:
            Result of base^exponent
        """
        result = round(base ** exponent, self.precision)
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def get_history(self) -> List[str]:
        """Get calculation history.
        
        Returns:
            List of all calculations performed
        """
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear calculation history."""
        self.history.clear()


def factorial(n: int) -> int:
    """Calculate factorial of a number.
    
    Args:
        n: Non-negative integer
        
    Returns:
        Factorial of n (n!)
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
    """
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def is_prime(n: int) -> bool:
    """Check if a number is prime.
    
    Args:
        n: Integer to check
        
    Returns:
        True if n is prime, False otherwise
        
    Examples:
        >>> is_prime(7)
        True
        >>> is_prime(10)
        False
    """
    if n < 2:
        return False
    
    if n == 2:
        return True
    
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    
    return True


if __name__ == "__main__":
    # Example usage
    calc = Calculator(precision=3)
    
    print("Calculator Demo")
    print("=" * 40)
    print(f"Addition: 10 + 5 = {calc.add(10, 5)}")
    print(f"Subtraction: 10 - 5 = {calc.subtract(10, 5)}")
    print(f"Multiplication: 10 * 5 = {calc.multiply(10, 5)}")
    print(f"Division: 10 / 5 = {calc.divide(10, 5)}")
    print(f"Power: 2 ^ 8 = {calc.power(2, 8)}")
    
    print("\nHistory:")
    for operation in calc.get_history():
        print(f"  {operation}")
    
    print(f"\nFactorial of 5: {factorial(5)}")
    print(f"Is 17 prime? {is_prime(17)}")
