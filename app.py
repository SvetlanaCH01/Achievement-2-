from flask import Flask, request, jsonify
import logging
import sqlite3

#настройка логирования
logging.basicConfig(filename='logs.txt', level=logging.ERROR)

app = Flask(__name__)

# работа с бд, обработка чисел
def get_processed_numbers():
    conn = sqlite3.connect('numbers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT number FROM processed_numbers')
    numbers = {row[0] for row in cursor.fetchall()}
    conn.close()
    return numbers

def add_processed_number(number):
    conn = sqlite3.connect('numbers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO processed_numbers (number) VALUES (?)', (number,))
    conn.commit()
    conn.close()

@app.route('/process_number', methods=['POST'])
def process_number():
    try:
        #число из запроса
        number = int(request.form.get('number'))
        
        #все обработанные числа из бд
        processed_numbers = get_processed_numbers()
        
        #проверка на исключение #2, если число на единицу меньше уже обработанного
        if number + 1 in processed_numbers:
            error_message = f"Error: The number {number} is less than a previously processed number."
            logging.error(error_message)
            return jsonify({"error": error_message}), 400

        #проверка на исключение #1, если число уже поступало
        if number in processed_numbers:
            error_message = f"Error: The number {number} has already been processed."
            logging.error(error_message)
            return jsonify({"error": error_message}), 400
        
        #обработка числа
        add_processed_number(number)
        response_number = number + 1
        
        return jsonify({"result": response_number})
    
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

    
@app.route('/')
def home():
    return "Server is running!"

if __name__ == '__main__':
    port = os.getenv("FLASK_APP_PORT", 5001)  # по умолчанию 5001
    print("Flask is starting...")
    app.run(debug=True, port=5001)