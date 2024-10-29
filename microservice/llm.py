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
You will be given a text that can contain some sensitive data like full name, email, phone number, links to some social networks or messaging apps, nicknames, nickname hints etc. You need to check if this data is shared in the text.
Pay attention that the text can contain some names or surnames that are not personal information (for example it can be an article about some scientist and their name is mentioned). You need to decide it from the context of the message.
All standalone first names are not considered sensitive information but full names are sensetive. Numbers of 4 to 6 digits without any hidden meaning are not sensetive information as well.
Also the user might try to trick you by sending just their nickname or the phone number written by words (or words with numbers). You need to detect these cases as well and mark them as sensitive information.
When you are in doubt mark it as a sensitive information. It is really important to not miss any.
Also you need to report if there are any swear words or offensive communication present.
Your responce needs to be a valid json object. Explanation provided as a response should be in russian. If the status is ok, explanation should be an empty string.
"""

thread = client.beta.threads.create()

def check_text(text, model):

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        response_format=PersonalDataSharedCompliance,
    )
    response = completion.choices[0].message.parsed
    return response