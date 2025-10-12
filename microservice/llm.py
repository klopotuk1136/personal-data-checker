from openai import OpenAI

client = OpenAI()


schema = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["ok", "sensitive_information", "swear_words", "offensive_communication"],
                "description": "Overall compliance status."
            },
            "explanation": {
                "type": "string",
                "description": "Optional explanation providing additional context."
            }
        },
        "required": ["status"],
        "additionalProperties": False
    }

prompt = """
Your purpose is to detect personal data sharing or inappropriate content in texts.
You will be given a text that may or may not contain some sensitive data like full name, email, phone number, links to some social networks or messaging apps, nicknames, nickname hints etc. You need to check if this data is shared in the text.
Pay attention that the text may contain some names or surnames that are not personal information (for example it can be an article about some scientist and their name is mentioned). You need to decide it from the context of the message.
If the name and surname are necessary for the message context and are not giving out personal data of the USERS themselves, then it should not be considered a sensetive information.
All standalone first names are not considered sensitive information but full names that may expose the identity of the user are sensetive. Numbers of 4 to 6 digits without any hidden meaning are not sensetive information as well.
Also the user might try to trick you by sending just their nickname or the phone number written by words (or words with numbers). You need to detect these cases as well and mark them as sensitive information.
When you are in doubt mark it as a sensitive information. It is really important to not miss any.
Also you need to report if there are any swear words or offensive communication present.
Your responce needs to be a valid json object. Explanation provided as a response should be in russian. If the status is ok, explanation should be an empty string.
"""

def check_text(text, model):

    response = client.responses.create(
        model=model,
        reasoning={"effort": "low"},
        text={
                "verbosity": "low",
                "format": {
                    "type": "json_schema",
                    "name": "PersonalDataSharedCompliance",
                    "schema": schema,
                    "strict": False
                }
            },
        input=[
            {
                "role": "developer",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ],
    )

    
    return response.output_text