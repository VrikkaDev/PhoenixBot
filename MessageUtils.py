global tr
tr = {}


def Init(textResponses):
    global tr
    tr = textResponses


class Answer:
    willRespond = False
    respondText = ""


def NeedToAnswer(message) -> Answer:
    text = message.content

    a = Answer()

    for key in tr.keys():

        value = tr[key]
        case_sensitive = True

        if value["case_sensitive"].lower() == "false":
            case_sensitive = False

        key_text = key
        message_text = text

        if not case_sensitive:
            key_text = key_text.lower()
            message_text = message_text.lower()

        if value["mode"] == "contains":
            if key_text in message_text:
                a.willRespond = True
                a.respondText = value["response"]
                break
        else:
            if message_text == key_text:
                a.willRespond = True
                a.respondText = value["response"]
                break
    return a
