from openai import OpenAI

client = OpenAI(base_url="https://api.deepseek.com")


schema = '''{
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
'''

check_message_prompt = f"""
Your purpose is to detect personal data sharing or inappropriate content in texts.
You will be given a text that may or may not contain some sensitive data like full name, email, phone number, links to some social networks or messaging apps, nicknames, nickname hints etc. You need to check if this data is shared in the text.
Pay attention that the text may contain some names or surnames that are not personal information (for example it can be an article about some scientist and their name is mentioned). You need to decide it from the context of the message.
If the name and surname are necessary for the message context and are not giving out personal data of the USERS themselves, then it should not be considered a sensetive information.
All standalone first names are not considered sensitive information but full names that may expose the identity of the user are sensetive. Numbers of 4 to 6 digits without any hidden meaning are not sensetive information as well.
Also the user might try to trick you by sending just their nickname or the phone number written by words (or words with numbers). You need to detect these cases as well and mark them as sensitive information.
When you are in doubt mark it as a sensitive information. It is really important to not miss any.
Also you need to report if there are any swear words or offensive communication present.
Your responce needs to be a valid json object. Explanation provided as a response should be in russian. If the status is ok, explanation should be an empty string.
The JSON must have the following schema: {schema}

EXAMPLE INPUT: 
Добрый день. Мне было бы удобнее общаться в телеграме - @my_best_tutor

EXAMPLE JSON OUTPUT:
{{
    "status": "sensitive_information",
    "explanation": "Telegram username is shared in the message"
}}

EXAMPLE INPUT: 
Добрый день. У меня вопросы по поводу Юрия Гогунского - нужно ли цитировать его статьи в моём дипломе?

EXAMPLE JSON OUTPUT:
{{
    "status": "ok",
    "explanation": ""
}}

EXAMPLE INPUT: 
Блять, когда уже будет готов мой диплом?

EXAMPLE JSON OUTPUT:
{{
    "status": "swear_words",
    "explanation": "В сообщении есть слово блять, что является ругательным"
}}

"""

def check_text(text, model):

    response = client.chat.completions.create(
        model=model,
        response_format={
            'type': 'json_object'
        },
        messages =[
            {
                "role": "system",
                "content": check_message_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ],
    )

    
    return response.choices[0].message.content

def send_request_to_llm(text, prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ],
    )
    return response.choices[0].message.content