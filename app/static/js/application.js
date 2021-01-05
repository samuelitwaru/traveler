// Support TLS-specific URLs, when appropriate.
var scheme = window.location.protocol == "https:" ? 'wss://' : 'ws://';
var webSocketUri =  scheme
                    + window.location.hostname
                    + (location.port ? ':'+location.port: '')
                    + '/submit';


function log(text){
  alert(text)
}

var websocket = new WebSocket(webSocketUri);

websocket.onopen = function() {
  log('Connected');
};

websocket.onclose = function() {
  log('Closed');
};

// websocket.onmessage = function(e) {
//   log('Message received');
//   output.append($('<li>').text(e.data));
// };

websocket.onerror = function(e) {
  log('Error (see console)');
  console.log(e);
};

// inbox.onmessage = function(message) {
//   console.log(">>>>>", message)
//   var data = JSON.parse(message.data);
//   $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text(data.handle).html() + "</div><div class='panel-body'>" + $('<span/>').text(data.text).html() + "</div></div>");
//   $("#chat-text").stop().animate({
//     scrollTop: $('#chat-text')[0].scrollHeight
//   }, 800);
// };

// inbox.onopen = function(){
//     console.log('inbox closed');
//     this.inbox = new WebSocket(inbox.url);

// };

// outbox.onopen = function(){
//     console.log('outbox closed');
//     this.outbox = new WebSocket(outbox.url);
// };

// $("#input-form").on("submit", function(event) {
//   event.preventDefault();
//   var handle = $("#input-handle")[0].value;
//   var text   = $("#input-text")[0].value;
//   outbox.send(JSON.stringify({ handle: handle, text: text }));
//   $("#input-text")[0].value = "";
// });

var socketSubmit = function(event){
  alert(event)
  event.preventDefault(); //prevent default action
  $(this).attr("action")
  var form = $(this)
  var handle = form[0].dataset.handle
  var form_data =  form.serialize(); //Encode form elements for submission
  console.log(">>>>>>>>>>>>", { handle: handle, data: form_data })
  // socket.emit(event, form_data);
  websocket.send(JSON.stringify({ handle: handle, data: form_data }));
}

$(".socketForm").on('submit', socketSubmit)
