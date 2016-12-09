from watson_developer_cloud import conversation_v1

json = """
{
  "intents": [
    {
      "intent": "destination",
      "confidence": 0.3521221876761777
    }
  ],
  "entities": [
    {
      "entity": "sys-date",
      "location": [
        0,
        7
      ],
      "value": "2016-12-09",
      "metadata": {
        "calendar_type": "GREGORIAN"
      }
    },
    {
      "entity": "sys-time",
      "location": [
        0,
        7
      ],
      "value": "18:00:00",
      "metadata": {
        "calendar_type": "GREGORIAN"
      }
    }
  ],
  "input": {
    "text": "tonight"
  },
  "output": {
    "log_messages": [],
    "text": [],
    "nodes_visited": [
      "node_4_1481308591294"
    ]
  },
  "context": {
    "conversation_id": "6f4f9f93-36a0-41f8-93d6-8bd72c98e7ab",
    "system": {
      "dialog_stack": [
        "node_4_1481308591294"
      ],
      "dialog_turn_counter": 3,
      "dialog_request_counter": 3
    },
    "departure": "BOS"
  }
}
"""

def getResponse(input_message):
    if input_message == None:
        input_message = ""
    return conversation_v1.message(workspace_id, input_message)

def getResponseTest():
    global json
    return json
