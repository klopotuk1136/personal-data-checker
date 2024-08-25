from openai import OpenAI
import json
assistant_id="asst_4T6HTRm5HVaccvxqR0eWenZo"

client = OpenAI()
thread = client.beta.threads.create()

def check_text(text):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            limit=1
        )
        return json.loads(messages.data[0].content[0].text.value)
    else:
        raise Exception(f"Assistant had {run.status} status.")