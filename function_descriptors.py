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
    },
    {
        "name": "trigger_notification_openai",
        "description": "Add a transaction to the database",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "integer",
                    "description": "The amount of transaction done.",
                },
                "type": {
                    "type": "string",
                    "description": "It tells that whether money is deposited to our account or transferred from somenone or withdrawn from atm. When money is transferred from my account give value of type argument as withdrawl and if money is getting deposited to my account give type as received.",
                    "enum": ["deposit", "received","withdrawal"]
                },
                "description": {
                    "type": "string",
                    "description": "Description of the transaction triggered",
                },
            },
            "required": ["amount", "type","description"],
        },
    },
    {
        "name": "pay_credit_card_bill_openai",
        "description": "Pay the credit card bill",
        "parameters": {
            "type": "object",
            "properties": {
                "credit_card_amt": {
                    "type": "integer",
                    "description": "Amount of credit card bill",
                },
                
            },
            "required": ["credit_card_amt"],
        },
    },
    {
        "name": "get_account_balance_openai",
        "description": "Get the current account balance",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "name of the bank account holder",
                },
                
            },
            # "required": ["credit_card_amt"],
        },
    },
    {
        "name": "get_account_statement_openai",
        "description": "Get the account statement",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "start date of the account statement",
                },
                "end_date": {
                    "type": "string",
                    "description": "end date of the account statement",
                },
                
            },
            "required": ["start_date","end_date"],
        },
    },
]
