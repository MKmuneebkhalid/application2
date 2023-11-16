import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    input_numbers = request.form['numbers']
    numbers_list = [float(n.strip()) for n in input_numbers.split(',') if n.strip()]

    # Your existing logic
    differences = calculate_differences(numbers_list)
    next_number = predict_next_number(differences, numbers_list)
    degree = min(len(numbers_list) - 1, 5)  # Adjust the degree if necessary
    polynomial = fit_polynomial(numbers_list, degree)

    output_str = f"Note: (You have entered {len(numbers_list)} comma separated numbers)\n\n"
    output_str += "Sequence of differences:\n"
    for diff in differences:
        output_str += " ".join(f"{d:+.2f}" for d in diff) + "\n"
    if next_number is not None:
        output_str += f"\n∴ The next number for given series is {next_number:.2f}\n"
    else:
        output_str += "\n∴ Could not predict the next number for the given series.\n"
    output_str += f"\nSolution-1\nGeneral polynomial is: {polynomial}\n"

    return render_template('result.html', result=output_str)

def calculate_differences(numbers):
    differences = []
    current_numbers = numbers
    while len(current_numbers) > 1:
        new_numbers = np.diff(current_numbers)
        differences.append(new_numbers)
        if len(set(new_numbers)) == 1:  # Stop if we reach a constant difference
            break
        current_numbers = new_numbers
    return differences

def predict_next_number(differences, numbers):
    if differences and len(differences[-1]) == 1:
        return numbers[-1] + differences[-1][0]
    return None

def fit_polynomial(numbers, degree):
    x = np.arange(1, len(numbers) + 1)
    coeffs = np.polyfit(x, numbers, degree)
    # Format the polynomial as a single line
    polynomial_terms = [f"{coeff:.4f}x^{degree-i}" for i, coeff in enumerate(coeffs)]
    polynomial_str = " + ".join(polynomial_terms).replace('x^0', '').replace(' + -', ' - ')
    return polynomial_str

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
