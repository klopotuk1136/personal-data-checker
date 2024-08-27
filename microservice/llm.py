from enum import Enum
from typing import Optional
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class Category(str, Enum):
    name_surname = "name and surname"
    email = "email"
    phone = "phone"
    link = "link"
    other = "other"

class PersonalDataSharedCompliance(BaseModel):
    is_personal_data_found: bool
    category: Optional[Category]
    explanation_if_found: Optional[str]

prompt = """
Your purpose is to detect personal data sharing in texts.
You will be given a text that can contain some personal data like name and surname, email, phone number, links to some social networks or messaging apps. You need to check if this data is shared in the text.
Your responce needs to be a valid json object.
Pay attention that the text can contain some names or surnames that are not personal information.You need to decide it from the context of the message
"""

thread = client.beta.threads.create()

def check_text(text):

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        response_format=PersonalDataSharedCompliance,
    )
    response = completion.choices[0].message.parsed
    return response