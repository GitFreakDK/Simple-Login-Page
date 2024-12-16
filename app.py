from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection details
DB_HOST = 'localhost'
DB_USER = 'root'  # Replace with your MySQL username
DB_PASSWORD = 'Kishore@2007'  # Replace with your MySQL password
DB_NAME = 'user_db_management' # Replace with your MySQL database name

def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        connection = None  
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
               
                cursor.execute("SELECT * FROM users WHERE email=%s OR phone=%s", (email, phone))
                user = cursor.fetchone()
                if user:
                    flash('Email or phone number already registered!')
                    return redirect(url_for('register'))

               
                cursor.execute(
                    "INSERT INTO users (firstname, lastname, email, phone, password) VALUES (%s, %s, %s, %s, %s)",
                    (firstname, lastname, email, phone, password)
                )
                connection.commit()

                
                cursor.execute(
                    "INSERT INTO office_details (phone, office_name, payments, total_work_hours, task_completion) VALUES (%s, NULL, 0.0, 0, NULL)",
                    (phone,)
                )
                connection.commit()

                print("Registration successful!")
                return render_template('success_register.html', firstname=firstname)

        except Exception as e:
            print(f"Error: {e}")
            flash(f"Error: {e}")
            return redirect(url_for('register'))

        finally:
            if connection:
                connection.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE (email=%s OR phone=%s) AND password=%s",
                    (identifier, identifier, password)
                )
                user = cursor.fetchone()
                if user:
                    cursor.execute("SELECT * FROM office_details WHERE phone=%s", (user[4],))
                    office_details = cursor.fetchone()
                    return render_template(
                        'success_login.html',
                        firstname=user[1],
                        lastname=user[2],
                        email=user[3],
                        phone=user[4],
                        office_details=office_details
                    )
                else:
                    flash('Invalid email/phone or password.')
                    return redirect(url_for('login'))

        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for('login'))

        finally:
            connection.close()

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)