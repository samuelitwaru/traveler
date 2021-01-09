function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.backTrigger').on('click', (event)=>{
    window.history.back()
})


// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};


var ws = new ReconnectingWebSocket(ws_scheme + location.host + "/ws");


var socketSubmit = function(event){
  event.preventDefault(); //prevent default action
  $(this).attr("action")
  var form = $(this)
  var handle = form[0].dataset.handle
  var form_data =  form.serialize(); //Encode form elements for submission
  ws.send(JSON.stringify({ handle: handle, data: form_data }));
}


var ajaxSubmit = function(event){
    event.preventDefault(); //prevent default action
    $(this).attr("action")
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
    var form_data = $(this).serialize(); //Encode form elements for submission
    var progressContainer = $(this)[0].dataset.progressContainer
    // var displayOverlay = $(this)[0].dataset.displayOverlay
    var patchContainers = JSON.parse($(this)[0].dataset.patchContainers)
    // if (displayOverlay){$('body').append(compontents["loadingOverlay"]}
    $(progressContainer).html(`
        <div class="d-flex justify-content-center">
            <div class="spinner-border text-info text-center" role="status" align="center">
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <p class="text-center">Please wait...</p>
    `)



    $.ajax({
        url : post_url,
        type: request_method,
        data : form_data,
    }).done(function(response){
        for (var i = 0; i < patchContainers.length; i++) {
            patchContainer = patchContainers[i]
            $(patchContainer).replaceWith(response.form_templates[patchContainer]);
        }
    })
}

var ajaxGetSubmit = function(event){
    target = event.target
    url = target.dataset.url    
    progressContainer = target.dataset.progressContainer    
    patchContainers = JSON.parse(target.dataset.patchContainers)
    loadUrl(url, progressContainer, patchContainers)
}


var ajaxMultipartSubmitForm = function(event){
    event.preventDefault(); //prevent default action
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
    var form_data = new FormData(this); //Creates new FormData object

    var progressContainer = $(this)[0].dataset.progressContainer
    var patchContainers = JSON.parse($(this)[0].dataset.patchContainers)
            
    $(progressContainer).html(`
        <div class="d-flex justify-content-center">
            <div class="spinner-border text-info" role="status" align="center">
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <p class="text-center">Please wait...</p>
    `)

    $.ajax({
        url : post_url,
        type: request_method,
        data : form_data,
        contentType: false,
        cache: false,
        processData:false
    }).done(function(response){
        for (var i = 0; i < patchContainers.length; i++) {
            patchContainer = patchContainers[i]
            $(patchContainer).replaceWith(response.form_templates[patchContainer]);
        }
    });
}


var loadUrl = function(url, progressContainer, patchContainers){
    $(progressContainer).html(`
        <div class="d-flex justify-content-center">
            <div class="spinner-border text-info" role="status" align="center">
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <p class="text-center">Please wait...</p>
    `)
    $.get(url, function(response) {
        for (var i = 0; i < patchContainers.length; i++) {
            patchContainer = patchContainers[i]
            $(patchContainer).replaceWith(response.form_templates[patchContainer]);
        }
    })
}


var loadTriggers = function(){
    $(".ajaxForm").on('submit', ajaxSubmit);
    $(".getRequestTrigger").on('click', ajaxGetSubmit); 
    $(".socketForm").on('submit', socketSubmit);
    $(".ajaxMultipartForm").on('submit', ajaxMultipartSubmitForm);
}

loadTriggers()

var printTicket = function(event) {
    data = event.dataset
    bus = data.bus
    seat = data.seat
    passenger = data.passenger
    pickup = data.pickup
    stop = data.stop
    fare = data.fare
    from = data.from
    to = data.to
    html = `
    <table class="table-bordered">
        <tboby>
            <tr>
                <td>Bus</td><td>${bus}</td>
            </tr>
            <tr>
                <td>Seat</td><td>${seat}</td>
            </tr>
            <tr>
                <td>Passenger</td><td>${passenger}</td>
            </tr>
            <tr>
                <td>From</td><td>${from}</td>
            </tr>
            <tr>
                <td>Stop</td><td>${stop}</td>
            </tr>
            <tr>
                <td>Fare</td><td>${fare}</td>
            </tr>
        </tbody>
    </table>
    `
    var originalContents = document.body.innerHTML;
    document.body.innerHTML = html
    window.print()
    document.body.innerHTML = originalContents;
    loadTriggers()
}


var calculateTimeLeft = function (stopTime){
    stopTime = new Date(stopTime)
    now = Date.now()
    // full time left in days
    var fullTimeLeft = (stopTime.getTime() - now) / 1000 / 3600 / 24
    // days
    days = Math.floor(fullTimeLeft)
    // hours
    hours = Math.floor((fullTimeLeft-days)*24)
    // minutes
    _mins = (fullTimeLeft-(days+(hours/24)))*24*60
    var mins = Math.floor(_mins)
        var secs = Math.floor((_mins-mins)*60)
    if (fullTimeLeft > 0){
        return `${days} days, ${hours} hours, ${mins} minutes, ${secs} seconds`
    }
    else {
        return "Finished <span class='fa fa-check'></span>"
    }
}

var setTimeLeft = function(widgetId){
    widget = $(widgetId)[0]
    stopTime = widget.dataset.stopTime
    timeLeft = calculateTimeLeft(stopTime)
    $(widgetId).html(timeLeft)
    setTimeout(()=>setTimeLeft(widgetId), 1000)
}


// front end compontent rendering
var compontents = {
    loadingOverlay: () => {
        template = `<div class="loader"></div>`
        return template
    },
    onlineStatusBox: (data) => {
        var isOnline = data["isOnline"]
        var part1 = isOnline ? "'text-success'>ONLINE" : "'text-danger'>OFFLINE"
        template = `<strong class=${part1}<strong>`
        return template
    },
}

var renderComponent = function(componentClass, data){
    template = compontents[componentClass](data)
    $(`.${componentClass}`).html(template)
}


// $(document).ready(function() {
//     $("[data-trigger]").on("click", function(e){
//         e.preventDefault();
//         e.stopPropagation();
//         var offcanvas_id =  $(this).attr('data-trigger');
//         $(offcanvas_id).toggleClass("show");
//         $('body').toggleClass("offcanvas-active");
//         $(".screen-overlay").toggleClass("show");
//     }); 

//     // Close menu when pressing ESC
//     $(document).on('keydown', function(event) {
//         if(event.keyCode === 27) {
//             $(".screen-overlay").removeClass("show");
//             $(".mobile-offcanvas").removeClass("show");
//             $("body").removeClass("offcanvas-active");
//         }
//     });

//     $(".btn-close, .screen-overlay").click(function(e){
//         $(".screen-overlay").removeClass("show");
//         $(".mobile-offcanvas").removeClass("show");
//         $("body").removeClass("offcanvas-active");
//     }); 
// });