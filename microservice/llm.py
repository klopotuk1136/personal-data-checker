def check_text(text):
    if 'Pavel' in text:
        return {"personal_data_found": True,
                "type": "Name"}
    else:
        return {"personal_data_found": False,
                "type": None}