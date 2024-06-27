from concurrent.futures import thread
import json
from openai import OpenAI

import logging
logger = logging.getLogger("django")

client = OpenAI(
  api_key="sk-proj-YVUxbVJmDP9ByWZ5WcL5T3BlbkFJDPKq2s6ARl1iGjsS5wCL"
)

def get_new_assistant():
    assistant_prompt = open("prompt", "r").read()
    assistant = client.beta.assistants.create(
        name="Interview",
        instructions=assistant_prompt,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o")
    return assistant

def get_new_thread():
  return client.beta.threads.create()

def create_new_message(thread_id, message):
  message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
  )
  return message

def run_thread(thread_id, assistant_id):
  if check_messages_to_run_thread(thread_id):
    run = client.beta.threads.runs.create_and_poll(
      thread_id=thread_id,
      assistant_id=assistant_id
    )
    if run.status != 'completed':
      raise Exception("FAILED_TO_RUN_THREAD")

  return get_messages(thread_id)

def check_messages_to_run_thread(thread_id):
  messages = get_raw_messages(thread_id)
  if messages:
    return messages[0].role == "user"
  return True

def get_messages(thread_id):
  messages = [{
    "message":parse_message(message.content[0].text.value),
    "role": message.role
    } for message in get_raw_messages(thread_id)]
  messages.reverse()
  return messages

def parse_message(message_text):
  return message_text.split("```json")[0]

def get_raw_messages(thread_id):
  try:
    return client.beta.threads.messages.list(thread_id=thread_id).data
  except Exception as e:
    return []

def get_result(messages):
    if not messages:
      return None
    last_message = messages[0].content[0].text.value
    json_split = last_message.split("```json")
    has_json = len(json_split) == 2
    if not has_json:
        return None
    return json.loads(json_split[1].split("```")[0])