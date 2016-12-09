from flask import Flask
from watson_developer_cloud import conversation_v1

app = Flask(__name__)



@app.route("/api/message")
def getResponse(workspace_id, input_message):
    if input_message == None:
        input_message = ""
    return conversation_v1.message(workspace_id, input_message)


if __name__ == "__main__":
    app.run()
