# from flask import Flask, render_template, jsonify, send_from_directory, request, send_file, make_response, Response
# from flask_socketio import SocketIO, emit
# import eventlet
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import requests
# from datetime import datetime,timedelta
# import csv
# import io
# import os
# import json
# import csv
# import pdfkit
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from io import StringIO


# client = MongoClient('mongodb://localhost:27017')
# db = client['bankdata']  # Replace with your database name
# collection = db['transactions']  # Replace with your collection name
# # app = Flask(__name__)
# # app.config['SECRET_KEY'] = 'your_secret_key'
# # app.config['DEBUG'] = True
# # socketio = SocketIO(app, async_mode='eventlet')
# documents = collection.find()
# filter = {}  # empty filter to update all documents
# update = {'$set': {'timestamp': datetime.now().timestamp()}}  # add the timestamp field with the current datetime value
# collection.update_many(filter, update)
# # Print each document

# start_date = "30-04-2023"
# end_date = "22-06-2023"
# date_format = "%d-%m-%Y"

# # Convert start_date and end_date to datetime objects
# start_datetime = datetime.strptime(start_date, date_format)
# end_datetime = datetime.strptime(end_date, date_format)


# # Convert datetime objects to timestamps
# start_timestamp = start_datetime.timestamp()
# end_timestamp = end_datetime.timestamp()
# documents = collection.find({
#         'timestamp': {
#             '$gte': start_timestamp,
#             '$lte': end_timestamp
#         }
#     })
# for document in documents:
#     print(document)


import nest_asyncio
nest_asyncio.apply() 

@socketio.on('get_response')
def handleMessage(data):
    try:
        t0 = time.time()
        req_vars = req_var_processing.orchestrator("get_response")(data)
        debug_dict = {
            "su_id": req_vars.su_id,
            "conversation_id": req_vars.conversation_id,
            "turn_id": req_vars.turn_id,
            "user_input": req_vars.msg
        }
        response, messages, intent, stream = get_response(req_vars.msg, req_vars.su_id, req_vars.is_new_chat, req_vars.api_response, req_vars.search_term)
        debug_dict.update({"Time taken for first token for socket" : "%s" %(time.time() - t0)})
        logger.debug(debug_dict)
        chat_response = ""
        temp_response = {"continue": False, "intent": "QnA", "message": "", "token_count": 0}
        if stream == True:
            if type(response) != dict:
                for chunk in response:
                    try:
                        response_text = chunk["choices"][0]["delta"]["content"] # type: ignore
                        # print(response_text)
                        # temp_response = intent_check("trigger_call_scheduler()", response_text, temp_response)
                        # temp_response = intents_check(response_text, temp_response)
                        # # print("temp_response in clover_vce: ", temp_response)
                        # if temp_response is not None and temp_response.get("continue") == True:
                        #     continue
                        # elif temp_response is not None:
                        #     response_text = temp_response.get("message", "")
                        #     intent = temp_response.get("intent", "QnA")
                        chat_response += response_text
                        if "trigger_call_scheduler()" in chat_response:
                            intent = "calendly_schedule"
                            print("triggering calendly")
                        if "end_conversation()" in chat_response:
                            intent = "user_feedback"
                            print("user_feedback")
                        # print("emitted response intent: %s" %(intent))
                        emit('new_response', {"system_text_response":response_text,"intent":intent})
                        # time.sleep(0.5)
                    except Exception as e:
                        warning = {"warning_at_backend":str(e), "traceback":str(traceback.format_exc())}
                        print(warning)
                        logger.debug(warning)
                        # response.update(data)
                        # emit("error", response)
            elif type(response) == dict and "exception_at_backend" in response:
                response.update(data)
                emit('error', response)
                return
        else:
            response.update(data)
            emit('new_response', {"system_text_response":response["system_text_response"],"intent":intent})

        emit('response_complete', "reponse generation complete")
        debug_dict.update({"Time taken for last token for socket" : "%s" %(time.time() - t0)})
        logger.debug(debug_dict)
        # print(messages)
        assistant_response = {"role": "assistant", "content": chat_response}
        # storefront_api_response = {"system_text_response": "", "intent": ""}
        messages.append(assistant_response)
        rc.set(req_vars.su_id, json.dumps(messages))
        print("Time taken: %s" %(time.time() - t0))
        debug_dict.update({"Time taken for completion of get_response" : "%s" %(time.time() - t0)})
        logger.debug(debug_dict)
        debug_dict.update({"messages": messages[1:]})
        logger.debug(debug_dict)
        data.update(debug_dict)
        logger.info(data)
        return
    except Exception as e:
        if hasattr(e, 'data'):
            response = e.data
        else:
            response = {
                "exception_at_backend":str(e),
                "traceback":str(traceback.format_exc()),
                "system_text_response": "Sorry, something went wrong",
                "retry_time": 60}
        response.update(data)
        emit("error", response)
        print("exception occured, response: %s" %(json.dumps(response)))
        logger.error(response)
        return
    
def get_response(user_input, su_id, is_new_chat, api_response, search_term):
    messages = get_user_message_history(su_id, is_new_chat, init_messages)
    api_assistant_message = api_manager.orchestrator(api_response)()

    super_editorial_response = super_editorial(user_input)
    if super_editorial_response is None:
        intent = "QnA"
        if search_term is not None:
            print("search_term: %s" %(search_term))
            messages.append({"role": "user", "content": "search_term: %s\nwelcome_message:" %(search_term)})
            return get_welcome_message(messages, stream=True), messages, intent, True
        elif api_assistant_message:
            messages.append({"role": "user", "content": api_assistant_message})
            return generate_completion(messages, stream=True), messages, intent, True
        else:
            messages.append({"role": "user", "content": user_input})
            clean_messages(messages)
            search_query = interpret_query(messages)
            # send to a webpage
            # notes = get_relevant_documents(search_query)
            # if "documents" in notes:
                # notes = notes["documents"]
            notes = str("notes")
            with open("query_messages.txt", "a") as f:
                f.write("\n\n")
                f.write("notes: %s" %(notes))
                f.write("\n\n")
            # send to a webpage
            # chat_response = generate_completion(messages, notes)
            print("duplicate test")
            return generate_completion(messages, stream=True), messages, intent, True
        # send to a webpage
    #     chat_response, intent = calendly_pre_schedule(chat_response, intent)
    else:
        chat_response, intent = super_editorial_response
        return chat_response, messages, intent, False
    # logger.info("chat_response: {}\n\n".format(chat_response))
    # assistant_response = {"role": "assistant", "content": chat_response}
    # storefront_api_response = {"system_text_response": chat_response, "intent": intent}
    # with open("system_text_response.txt", "w") as f:
    #     f.write(json.dumps((messages), indent=4))
    #     f.write("\n\n")
    #     f.write(json.dumps((storefront_api_response), indent=4))
    # # send to a webpage
    # messages.append(assistant_response)
    # rc.set(su_id, json.dumps(messages))
    # return storefront_api_response