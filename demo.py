from dotenv import load_dotenv
from langchain import OpenAI 
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.agents import create_csv_agent
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

load_dotenv()

filepath = "test_data.csv"
loader = CSVLoader(filepath, csv_args={ 'delimiter': ',' }, encoding='utf-8')
data = loader.load()

def generate_answer(question):
    llm = OpenAI(temperature=0)

    agent = create_csv_agent(llm, filepath, verbose=True)
    response = agent.run(question)
    # model_engine = "text-davinci-002"
    # prompt = (f"Q: {question}\n"
    #           "A:")

    # response = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=prompt,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )

    # answer = response.choices[0].text.strip()
    return response


# Define a route to handle incoming requests
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    # Generate the answer using GPT-3
    answer = generate_answer(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)


# print(data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
# ques = "How many types of account type are there and also tell me the name and count of each type?"
# generate_answer(ques)
# agent = create_csv_agent(llm, filepath, verbose=True)
# agent.run("How many types of account type are there and also tell me the name and count of each type?")
# agent.run("What does this csv tell about?")
# agent.run("What is the most common interest rate?")