import langchain
import pymongo

def chatbot(message):
    chain = langchain.chains(
        prompt_template="Question: {question} Answer: {answer}",
        llm=langchain.HuggingFacePipeline("davinci-code"),
    )

    # Connect to the MongoDB database
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['bankdata']
    collection = db['transactions']

    # Find the documents that match the question
    documents = collection.find({"question": message})

    # If there are any documents, use the LLM to answer the question
    if documents:
        document = documents[0]
        response = chain.run(question=message, document=document)
        return response["answer"]
    else:
        return "I don't know the answer to that question."

message = "What is the capital of France?"
response = chatbot(message)
print(response)
