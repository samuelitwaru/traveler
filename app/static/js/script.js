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


var ajaxSubmit = function(event){
    event.preventDefault(); //prevent default action
    $(this).attr("action")
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
    var form_data = $(this).serialize(); //Encode form elements for submission
    var progressContainer = $(this)[0].dataset.progressContainer
    var patchContainers = JSON.parse($(this)[0].dataset.patchContainers)

    $(progressContainer).html(`
        <div class="spinner-border text-info" role="status" align="center">
            <span class="sr-only">Loading...</span>
        </div>
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

var socketSubmit = function(event){
    event.preventDefault(); //prevent default action
    $(this).attr("action")
    var form = $(this)
    var event = form[0].dataset.event
    var form_data =  form.serialize(); //Encode form elements for submission
    socket.emit(event, form_data);
}

$(".ajaxForm").on('submit', ajaxSubmit)
$(".socketForm").on('submit', socketSubmit)

var ajaxMultipartSubmitForm = function(event){
    event.preventDefault(); //prevent default action
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
    var form_data = new FormData(this); //Creates new FormData object

    var progressContainer = $(this)[0].dataset.progressContainer
    var patchContainers = JSON.parse($(this)[0].dataset.patchContainers)
            
    $(progressContainer).html(`
            <div class="spinner-border text-info" role="status" align="center">
                <span class="sr-only">Loading...</span>
            </div>
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

$(".ajaxMultipartForm").on('submit', ajaxMultipartSubmitForm);