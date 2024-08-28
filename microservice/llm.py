from enum import Enum
from typing import Optional
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class Status(str, Enum):
    ok = "ok"
    sensitive_information = "sensitive_information"
    swear_words = "swear_words"
    offensive_communication = "offensive_communication"

class PersonalDataSharedCompliance(BaseModel):
    status: Status
    explanation: Optional[str]

prompt = """
Your purpose is to detect personal data sharing or inappropriate content in texts.
You will be given a text that can contain some sensitive data like name and surname, email, phone number, links to some social networks or messaging apps. You need to check if this data is shared in the text.
Also you need to report if there are any swear words or offensive communication present.
Your responce needs to be a valid json object.
Pay attention that the text can contain some names or surnames that are not personal information (for example it can be an article about some scientist and their name is mentioned). You need to decide it from the context of the message
"""

thread = client.beta.threads.create()

def check_text(text):

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        response_format=PersonalDataSharedCompliance,
    )
    response = completion.choices[0].message.parsed
    return response