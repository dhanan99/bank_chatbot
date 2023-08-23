# import langchain
# import pymongo

# def chatbot(message):
#     chain = langchain.chains(
#         prompt_template="Question: {question} Answer: {answer}",
#         llm=langchain.HuggingFacePipeline("davinci-code"),
#     )

#     # Connect to the MongoDB database
#     client = pymongo.MongoClient('mongodb://localhost:27017')
#     db = client['bankdata']
#     collection = db['transactions']

#     # Find the documents that match the question
#     documents = collection.find({"question": message})

#     # If there are any documents, use the LLM to answer the question
#     if documents:
#         document = documents[0]
#         response = chain.run(question=message, document=document)
#         return response["answer"]
#     else:
#         return "I don't know the answer to that question."

# message = "What is the capital of France?"
# response = chatbot(message)
# print(response)



from dateutil.parser import parse

def convert_to_dd_mm_yyyy(date_string):
    try:
        date_object = parse(date_string)
        formatted_date = date_object.strftime('%d-%m-%Y')
        return formatted_date
    except ValueError:
        return "Invalid date format"

# Examples
date_strings = [
    "2023-08-19",
    "08/19/2023",
    "19-08-2023 14:30:00",
    "Friday, August 19, 2023",
    "08-19/2023"
]

for date_string in date_strings:
    formatted_date = convert_to_dd_mm_yyyy(date_string)
    print(f"Input: {date_string}, Formatted: {formatted_date}")