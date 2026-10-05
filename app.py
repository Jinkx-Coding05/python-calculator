# app.py
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    # history.db naam ki file automatically ban jayegi
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    # Ek table banate hain agar wo pehle se nahi bani hui hai
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Jaise hi app run hogi, ye function table bana dega
init_db()
# ----------------------

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    
    if request.method == 'POST':
        try:
            num1 = float(request.form.get('number1'))
            num2 = float(request.form.get('number2'))
            operation = request.form.get('operation')
            
            # Sign store karne ke liye variables
            sign = ''
            
            if operation == 'add':
                result = num1 + num2
                sign = '+'
            elif operation == 'subtract':
                result = num1 - num2
                sign = '-'
            elif operation == 'multiply':
                result = num1 * num2
                sign = '×'
            elif operation == 'divide':
                if num2 == 0:
                    result = "Error: Cannot divide by zero!"
                    sign = '÷'
                else:
                    result = round(num1 / num2, 4) # 4 decimal places tak
                    sign = '÷'
            
            # Data save karne ka logic (Sirf tab jab valid numbers hon)
            if sign:
                # Expression banaya jaise: "5.0 + 10.0"
                expression = f"{num1} {sign} {num2}" 
                
                # Database me insert karna
                conn = sqlite3.connect('history.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO calculations (expression, result) VALUES (?, ?)", (expression, str(result)))
                conn.commit()
                conn.close()
                
        except ValueError:
            result = "Error: Please enter valid numbers!"

    # --- History Fetch Karna ---
    # Page load hone par aur calculate hone ke baad, last 5 records nikalenge (ORDER BY id DESC)
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT expression, result FROM calculations ORDER BY id DESC LIMIT 5")
    history = cursor.fetchall() # Ye list of tuples dega, eg: [('5.0 + 5.0', '10.0')]
    conn.close()
    
    # render_template me history variable pass kar rahe hain
    return render_template('index.html', result=result, history=history)

if __name__ == '__main__':
    app.run(debug=True)