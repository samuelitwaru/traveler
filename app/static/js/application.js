// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};


var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");


var socketSubmit = function(event){
  event.preventDefault(); //prevent default action
  $(this).attr("action")
  var form = $(this)
  var handle = form[0].dataset.handle
  var form_data =  form.serialize(); //Encode form elements for submission
  outbox.send(JSON.stringify({ handle: handle, data: form_data }));
}

$(".socketForm").on('submit', socketSubmit)
