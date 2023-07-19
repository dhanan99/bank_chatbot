from pymongo import MongoClient

# Establish a connection to MongoDB
client = MongoClient('mongodb://localhost:27017')

# Access the desired database
db = client['bankdata']

# Access the desired collection
collection = db['transactions']

# Define the data to be inserted
data = [
    { 'type': 'deposit', 'amount': 1000, 'date': '2023-05-01', 'description': 'Salary deposit' },
    { 'type': 'withdrawal', 'amount': 500, 'date': '2023-05-02', 'description': 'Grocery shopping' },
    # Add more data entries here...
]

# Insert the data into the collection
result = collection.insert_many(data)

# Print the number of inserted documents
print(f"Inserted {len(result.inserted_ids)} documents")
