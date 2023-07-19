from flask import Flask, render_template, jsonify, send_from_directory, request, send_file, make_response, Response
from flask_socketio import SocketIO, emit
import eventlet
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
from datetime import datetime,timedelta
import csv
import io
import os
import json
import csv
import pdfkit
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import StringIO
import openai
from dotenv import load_dotenv

load_dotenv()

client = MongoClient('mongodb://localhost:27017')
db = client['bankdata']  # Replace with your database name
collection = db['transactions']  # Replace with your collection name
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG'] = True
socketio = SocketIO(app, async_mode='eventlet')
openai.api_key = os.getenv('OPENAI_API_KEY')
# from flask import Flask, render_template, jsonify

# app = Flask(__name__)

# Existing routes for account statement and other functionality

# Route to fetch chat messages (replace this with your actual implementation)
function_descriptions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "description": "The temperature unit to use. Infer this from the users location.",
                            "enum": ["celsius", "fahrenheit"]
                        },
                    },
                    "required": ["location", "unit"],
                },
            }
        ]
def get_current_weather(location, unit):
    
    """Get the current weather in a given location"""
    
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

@app.route('/save_message', methods=['POST'])
def save_message():
    message = request.json['message']
    # Process the message (e.g., save it to a database, perform any necessary operations)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        
        # This is the chat message from the user
        messages=[{"role": "user", "content": message}],
    
        
        functions=function_descriptions,
        function_call="auto",
    )

    ai_response_message = response["choices"][0]["message"]
    print(ai_response_message)

    user_location = eval(ai_response_message['function_call']['arguments']).get("location")
    user_unit = eval(ai_response_message['function_call']['arguments']).get("unit")
    function_response = get_current_weather(
    location=user_location,
    unit=user_unit,
    )


    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": message},
            ai_response_message,
            {
                "role": "function",
                "name": "get_current_weather",
                "content": function_response,
            },
        ],
    )

    oupt = second_response['choices'][0]['message']['content']
    print(oupt)
    response = {'output': oupt}
    return jsonify(response)
@app.route('/data')
def get_data():
    data = list(collection.find())
    json_data = []
    for doc in data:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
        json_data.append(doc)
    return jsonify(data)

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory('static', filename)

@app.route('/css/<filename>')
def get_css(filename):
    return send_from_directory('css', filename)

@app.route('/')
def index():
    return render_template('mainpg.html')

@app.route('/trigger-notification')
def trigger_notification():
    data = {
        'message': 'A transaction has been triggered!',
        'amount': 22200.0,
        'type': 'Deposit',
        'date': datetime.now().strftime('%d-%m-%Y'),
        'description': 'salary',
        'timestamp': datetime.now().timestamp()
    }
    data["_id"] = str(ObjectId())
    collection.insert_one(data)
    socketio.emit('notification', data)
    return jsonify(data)


@app.route('/account_balance')
def get_account_balance():
    # Calculate the account balance by summing the transaction amounts
    pipeline = [
    {
        '$group': {
            '_id': None,
            'balance': {
                '$sum': {
                    '$cond': [
                        {'$eq': [{'$toLower': '$type'}, 'withdrawal']},
                        {'$multiply': ['$amount', -1]},
                        '$amount'
                        ]
                    }
                }
            }
        }
    ]
    result = list(collection.aggregate(pipeline))

    if len(result) > 0:
        account_balance = result[0]['balance']
    else:
        account_balance = 0.0

    return jsonify({'balance': account_balance})

@app.route('/pay_bill')
def pay_credit_card_bill():
    response = get_account_balance()
    account_balance = response.json.get('balance')
    credit_card_bill = 330  # Assuming the bill amount is sent in the request JSON

    if account_balance >= credit_card_bill:
        # Proceed to pay the bill
        new_balance = account_balance - credit_card_bill
        withdrawal_data = {
            'type': 'Withdrawal',
            'amount': credit_card_bill,
            'date': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'description': 'Credit card bill payment',
            'timestamp': datetime.now().timestamp()
        }
        withdrawal_data["_id"] = str(ObjectId())
        collection.insert_one(withdrawal_data)
        
        # Return a success message
        withdrawal_data["message"] = 'Credit card bill of current month has been paid!'
        socketio.emit('new_transaction', withdrawal_data)
        socketio.emit('notification', {'balance': new_balance})
        return jsonify({'message': 'Payment successful!'})
    else:
        # Return an error message
        withdrawal_data["message"] = 'Insufficient funds to pay the bill.'
        socketio.emit('new_transaction', withdrawal_data)
        socketio.emit('notification', {'balance': new_balance})
        return jsonify({'message': 'Insufficient funds to pay the bill.'})

@app.route('/account_statement', methods=['GET'])
def get_account_statement():
    
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    date_format = "%d-%m-%Y"

    # Convert start_date and end_date to datetime objects
    start_datetime = datetime.strptime(start_date, date_format).timestamp()
    end_datetime = datetime.strptime(end_date, date_format).timestamp()
    
    print(start_date)
    print(end_date)
    # end_date += timedelta(days=1)
    # Query the transactions collection for transactions within the date range
    filtered_transactions = collection.find({
        'timestamp': {
            '$gte': start_datetime,
            '$lte': end_datetime
        }
    })
    
    # transaction_data = []
    # for transaction in filtered_transactions:
    #     transaction_data.append(transaction_dict)
    csv_data = [['Date', 'Description', 'Amount']]

    for transaction in filtered_transactions:
        csv_data.append([
            transaction['date'],
            transaction['description'],
            transaction['amount']
        ])

    # Create a string buffer to write the CSV data
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(csv_data)

    # Create the response with the CSV data
    response = Response(csv_buffer.getvalue(), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='account_statement.csv')

    return response
        
if __name__ == '__main__':
    socketio.run(app)
