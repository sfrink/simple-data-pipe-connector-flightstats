from watson_developer_cloud import ConversationV1
from pixiedust.utils.template import *
from .running.flightAccess import *
import pixiedust
import json
import traceback

myLogger = pixiedust.getLogger(__name__)

env = PixiedustTemplateEnvironment()

def getResponse(payload):
    conversation = ConversationV1(
        username='ed760194-a00a-4449-a52b-c4c185dda8fd',
        password='aG1eCCGeQirb',
        version='2016-09-20')

    workspace_id = "b46837f1-31bd-4e37-9551-104c44b7e46c"

    myLogger.info("payload to convo {0}".format(payload))
    if "context" in payload and "flight_number" in payload["context"] and "flightStatData" in payload["context"] :
        parts=payload["context"]["flight_number"].split("-")
        airline,flight = (parts[0], parts[1])
        flightStats = payload["context"]["flightStatData"]
        airlineData = None
        if flightStats["airlines"]:
            for airline in flightStats["airlines"]:
                if(airline["fs"] == airline):
                    airlineData = airline
                    break

        if airlineData is not None:
            payload["context"]["airlineData"] = airlineData


    result = conversation.message(workspace_id=workspace_id, message_input=payload['input'],context=payload['context'])
    myLogger.info("results from convo {0}".format(result))

    try:
        html, rightHtml = buildContentFromExternalSource(result)
        if html:
            myLogger.info("Trigger flight list")
            if "output" not in result:
                result["output"]={}
            result["output"]["html"] = html
        if rightHtml:
            myLogger.info("Got html")
            if "output" not in result:
                result["output"] = {}
            result["output"]["rightHtml"] = rightHtml;

    except Exception as e:
        myLogger.error("Unexpected Error:\n"+str(e)+"\n\n"+traceback.format_exc())

    return json.dumps(result)

def buildContentFromExternalSource(result):
    if "context" not in result:
        return None, None

    context = result["context"]
    html = None
    rightHtml = None
    if "departure_date" in context and "destination" in context and "departure" in context and "departure_time" in context and "layover" in context and "lookedUp" not in context:
        myLogger.info("going to try to get flights now....")
        flightStatData = getFlightsBetweenAirports(context["departure"], context["destination"], context["departure_date"])
        flights = flightStatData["scheduledFlights"]
        myLogger.info("flights {0}".format(json.dumps(flights)))
        context["lookedUp"] = "True"
        #context["flightStatData"] = flightStatData
        airports = flightStatData["airports"]
        for airport in airports:
            if airport["fs"] is context["destination"]:
                context["destLong"] = airport["longitude"]
                context["destLat"] = airport["latitude"]
            elif airport["fs"] is context["departure"]:
                context["deptLong"] = airport["longitude"]
                context["deptLat"] = airport["latitude"]
        flightStatData["airports"] = None
 
        html = env.getTemplate("convoPaths/flightLists.html").render(flights = flights)

    elif "check_weather" in context and "destination" in context:
        myLogger.info("getting the weather for {0}".format(context["destination"]))
        rightHtml = "<div> <b>this is the weather</b></div>"

    elif "check_airport_info" in context and "destination" in context: 
        myLogger.info("getting the airport info for {0}".format(context["destination"]))
        rightHtml = "<div> <b>this is the airport info</b></div>"
    elif "check_flight_info" in context and "flight_number" in context: 
        myLogger.info("getting the info for {0}".format(context["flight_number"]))
        rightHtml = "<div> <b>this is the flight_number info</b></div>"
    elif "predict_delay" in context: 
        myLogger.info("checking for delay {0}".format(context["destination"]))
        rightHtml = "<div> <b>this is the delay info</b></div>"
    return html, rightHtml
    