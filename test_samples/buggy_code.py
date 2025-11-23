"""
Sample buggy code for testing the AI Code Reviewer.
This file contains intentional bugs and optimization opportunities.
"""

def calculate_average(numbers):
    """Calculate average of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: Division by zero if empty list


def fetch_user_data(user_id):
    """Fetch user data from database."""
    query = "SELECT * FROM users WHERE id = " + str(user_id)  # Bug: SQL injection vulnerability
    # Execute query here
    return query


def process_items(items):
    """Process a list of items."""
    result = []
    for i in range(len(items)):  # Optimization: Use enumerate or direct iteration
        item = items[i]
        if item != None:  # Style: Should use 'is not None'
            result.append(item)
    return result


class DataManager:
    """Manages data operations."""
    
    def __init__(self):
        self.data = []
        self.cache = {}
    
    def add_data(self, value):
        """Add data to the list."""
        self.data.append(value)
        # Bug: No validation of input
        # Optimization: Missing cache invalidation
    
    def get_data(self, index):
        """Get data by index."""
        return self.data[index]  # Bug: No bounds checking


def find_maximum(arr):
    """Find maximum value in array."""
    max_val = arr[0]  # Bug: Assumes array is not empty
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val


# Global variable usage (code smell)
counter = 0

def increment_counter():
    """Increment global counter."""
    global counter
    counter = counter + 1  # Optimization: Could use += operator


if __name__ == "__main__":
    # Test code with bugs
    numbers = []
    avg = calculate_average(numbers)  # Will crash
    print(f"Average: {avg}")
