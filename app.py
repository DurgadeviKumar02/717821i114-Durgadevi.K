from flask import Flask, jsonify, request
import random
import math

app = Flask(__name__)

# Helper function to generate Fibonacci sequence
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Helper function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Helper function to generate random numbers
def generate_random_numbers(count):
    return [random.randint(1, 100) for _ in range(count)]

# Endpoint to calculate average of qualified numbers
@app.route('/numbers/<string:number_id>', methods=['GET'])
def calculate_average(number_id):
    numbers = request.args.get('numbers')
    if numbers is None:
        return jsonify({'error': 'No numbers provided'}), 400

    numbers = [int(num) for num in numbers.split(',')]

    qualified_numbers = []
    for num in numbers:
        if number_id == 'p' and is_prime(num):
            qualified_numbers.append(num)
        elif number_id == 'f' and num in fibonacci(20):  # Limit Fibonacci sequence to 20 numbers
            qualified_numbers.append(num)
        elif number_id == 'e' and num % 2 == 0:
            qualified_numbers.append(num)
        elif number_id == 'r':
            qualified_numbers.extend(generate_random_numbers(len(numbers)))
        else:
            return jsonify({'error': 'Invalid number ID or number provided'}), 400

    if not qualified_numbers:
        return jsonify({'error': 'No qualified numbers found'}), 404

    average = sum(qualified_numbers) / len(qualified_numbers)
    return jsonify({'average': average})

if __name__ == '__main__':
    app.run(debug=True)
