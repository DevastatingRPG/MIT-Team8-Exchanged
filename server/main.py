from flask import Flask, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'beansbestcat'
app.config['MYSQL_DB'] = 'exchange_rate'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    years = []  # Initialize a list to store the extracted years
    selected_year = ''
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        print(userDetails)
        selected_year = userDetails['year']  # Fetching the selected year

        # Display the selected year (optional)
        print(f"Selected Year: {selected_year}")

    # Query the database to extract years
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT Date FROM _2012")  # Ensure the table name is correct
    result = cur.fetchall()
    # print(result)
    # Extract years from the query result
    for row in result:
        date_str = row[0]  # Assuming date is in the first column
        # Convert string to datetime object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Convert date string to datetime object
        years.append(date_obj.year)  # Extract the year and add to the list

    cur.close()

    # Get unique years
    years = list(set(years))

    # Print all extracted years to the terminal
    print("Extracted Years:", years)

    return {'message': f"Years extracted and printed in the terminal. {selected_year}", 'data': result  }# Optional response to the user

if __name__ == '__main__':
    app.run(debug=True)