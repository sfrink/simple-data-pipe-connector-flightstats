from watson_developer_cloud import ConversationV1
import pixiedust
import json

myLogger = pixiedust.getLogger(__name__)

def getResponse(payload):
    conversation = ConversationV1(
        username='ed760194-a00a-4449-a52b-c4c185dda8fd',
        password='aG1eCCGeQirb',
        version='2016-09-20')

    workspace_id = "b46837f1-31bd-4e37-9551-104c44b7e46c"

    myLogger.info(payload)
    result = json.dumps(conversation.message(workspace_id=workspace_id, message_input=payload['input'],
                                             context=payload['context']))
    myLogger.info(result)
    return result
