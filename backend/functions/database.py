import os
import json
import random

# Get recent messages
def get_recent_messages():
  
  # Define the file name
  file_name = "stored_data.json"
  learn_instruction = {"role": "system", 
                       "content": "You are interviewing the user for a job as restaurant manager. Ask short questions that are relevant to the restautant manager position. Your name is rachel. The user is called Benedict. Keep your answers to under 30 words. "}
  
  # Initialize messages
  messages = []

  # Add Random Element
  x = random.uniform(0, 1)
  if x < 0.5:
    learn_instruction["content"] = learn_instruction["content"] + " Your response will have some dry humour. "
  else:
    learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather challenging question. "
  
  # Append instruction to message
  messages.append(learn_instruction)
  print(f"messages ==>: {messages}")

  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append last 5 rows of data
      if data:
        if len(data) < 5:
          for item in data:
            messages.append(item)
        else:
          for item in data[-5:]:
            messages.append(item)
  except Exception as e:
    print(e)

  return messages

# Stored Messages
def store_messages(request_message, response_message):

  # Define the file name
  file_name = "stored_data.json"  
  
  # Get recent messages
  messages = get_recent_messages()[1:]

  # Add messages to the data
  user_message = {"role": "user", "content": request_message}
  assistant_message = {"role": "assistant", "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the data to the file
  with open(file_name, "w") as f:
    json.dump(messages, f)

  # Reset the database file
def reset_messages():
  file_name = "stored_data.json"
  open(file_name, "w")