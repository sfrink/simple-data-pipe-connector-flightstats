// The Api module is designed to handle all interactions with the server

{%import "commonExecuteCallback.js" as commons%}

var Api = (function() {
  var requestPayload;
  var responsePayload;
  var messageEndpoint = '/api/message';

  // Publicly accessible methods defined
  return {
    sendRequest: sendRequest,

    // The request/response getters/setters are defined here to prevent internal methods
    // from calling the methods without any of the callbacks that are added elsewhere.
    getRequestPayload: function() {
      return requestPayload;
    },
    setRequestPayload: function(newPayloadStr) {
      requestPayload = JSON.parse(newPayloadStr);
    },
    getResponsePayload: function() {
      return responsePayload;
    },
    setResponsePayload: function(newPayloadStr) {
      debugger;
      responsePayload = JSON.parse(newPayloadStr);
    }
  };

  // Send a message request to the server
  function sendRequest(text, context) {
    // Build request payload
    var payloadToWatson = {};

    text = text || '';

    payloadToWatson.input = {
      text: text
    };

    payloadToWatson.context = context || {};

    var $$pixiedust_command = "from pixiedust_flightpredict.watsonMessageAPI import *" +
          "\nprint(getResponse(" + JSON.stringify(payloadToWatson) + "))";

    {% call(results) commons.ipython_execute("$$pixiedust_command", prefix) %}
      {% if results["error"] %}
        alert('error!');
      {% else %}
        {% if results != '' %}
          Api.setResponsePayload({{results}});
        {% endif %}
      {% endif %}
    {% endcall %}
  }
}());
