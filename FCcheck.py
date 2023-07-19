import openai
import json

# Environment Variables
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
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

user_query = "How are you?"

response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        
        # This is the chat message from the user
        messages=[{"role": "user", "content": user_query}],
    
        
        functions=function_descriptions,
        function_call="auto",
    )

ai_response_message = response["choices"][0]["message"]
print(ai_response_message)

user_location = eval(ai_response_message['function_call']['arguments']).get("location")
user_unit = eval(ai_response_message['function_call']['arguments']).get("unit")

def get_current_weather(location, unit):
    
    """Get the current weather in a given location"""
    
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

function_response = get_current_weather(
    location=user_location,
    unit=user_unit,
)


second_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "user", "content": user_query},
        ai_response_message,
        {
            "role": "function",
            "name": "get_current_weather",
            "content": function_response,
        },
    ],
)

print (second_response['choices'][0]['message']['content'])
