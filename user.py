from flask import Flask, request, render_template_string

app = Flask(__name__)

# Luhn Algorithm for validating card numbers
def luhn_algorithm(card_number):
    digits = [int(char) for char in str(card_number)][::-1]
    doubled_digits = [
        digit * 2 if index % 2 == 1 else digit for index, digit in enumerate(digits)
    ]
    processed_digits = [
        digit - 9 if digit > 9 else digit for digit in doubled_digits
    ]
    total_sum = sum(processed_digits)
    return total_sum % 10 == 0

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        card_number = request.form["card_number"]
        user_agent = request.headers.get("User-Agent")

        if card_number.isdigit():
            is_valid = luhn_algorithm(card_number)
            result = "VALID" if is_valid else "INVALID"
        else:
            result = "Please enter a valid card number."

        return render_template_string('''
            <h2>Card Number Validation Result</h2>
            <p>Card Number: {{ card_number }} - {{ result }}</p>
            <p>User Agent: {{ user_agent }}</p>
            <a href="/">Check Another Card</a>
        ''', card_number=card_number, result=result, user_agent=user_agent)
    
    return '''
        <h2>Enter Card Number for Validation</h2>
        <form method="POST">
            Card Number: <input type="text" name="card_number" />
            <input type="submit" value="Validate" />
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

