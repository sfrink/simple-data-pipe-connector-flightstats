from watson_developer_cloud import ConversationV1
from pixiedust.utils.template import *
from .running.flightAccess import *
import pixiedust
import json

myLogger = pixiedust.getLogger(__name__)

env = PixiedustTemplateEnvironment()

def getResponse(payload):
    conversation = ConversationV1(
        username='ed760194-a00a-4449-a52b-c4c185dda8fd',
        password='aG1eCCGeQirb',
        version='2016-09-20')

    workspace_id = "b46837f1-31bd-4e37-9551-104c44b7e46c"

    myLogger.info("payload {0}".format(payload))
    result = conversation.message(workspace_id=workspace_id, message_input=payload['input'],context=payload['context'])
    myLogger.info("results {0}".format(result))

    try:
        html = showFlightList(result)
        if html:
            myLogger.info("Trigger flight list")
            if "output" not in result:
                result["output"]={}
            result["output"]["html"] = html
    except:
        myLogger.error("Crap got an error")

    return json.dumps(result)

def showFlightList(result):
    if "context" not in result:
        return None

    context = result["context"]
    if "departure_date" in context and "destination" in context and "departure" in context and "departure_time" in context and "layover" in context:
        flights = getFlights(context["departure"], context["departure_date"], context["departure_time"])["scheduledFlights"]
        flights = [ f for f in flights if f["arrivalAirportFsCode"] == context["destination"]]
        myLogger.info("flights {0}".format(json.dumps(flights)))

        return env.getTemplate("convoPaths/flightLists.html").render(flights = flights)

    return None