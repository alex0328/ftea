$(document).ready(function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

// function dodaj loadery
    const taski_lista = document.getElementById('taski');
    console.log(taski_lista);

$.ajax({
    url: "/ff-ajax/", //gdzie się łączymy
    method: "post", //typ połączenia, domyślnie get
    dataType: "json", //typ danych jakich oczekujemy w odpowiedzi

    contentType: "application/json", //gdy wysyłamy dane czasami chcemy ustawić ich typ,
    success: function (request) {
        console.log(request);
        console.log(request['filter']['1']['fields']['description']);
        let loader = document.getElementsByClassName('loader-active');
        for (i=0; i<loader.length; i++) {
            loader[i].classList.add('noactive');
        }
        let placesList = findPlaces();
        placesList[0].innerHTML = request['filter_count'];
        placesList[1].innerHTML = request['all_task_count'];
        placesList[2].innerHTML = request['all_done'];

        placesList[3].innerHTML = request['filter'][1]['fields']['description'];
        console.log(request['filter']);
        console.log(createElement('li'));
        console.log(createElement('span'));
        console.log(createElement('div'));
        },

    error: function (request, status, error) {
        alert(status);
    }
});

    function extract(request, parameter) {
        let extracted = request[parameter];
        return extracted
    }

    function findPlaces() {
        let issuesCount = document.getElementById('issues-count'),
            allIssuesCount = document.getElementById('all-issues-count'),
            allDone = document.getElementById('all-done'),
            placeTaskList = document.getElementById('placeTaskList');
        return [issuesCount, allIssuesCount, allDone, placeTaskList];
    }

    function createStructure() {
        createElement('li');
        createElement('a');
        createElement('div');
    }
function createElement(element) {
    return document.createElement(element)
}


});

// <li>
//                                   <a href="#" class="task-frame {{ issue.fields.priority }}" id="{{ issue.id }}">
//                                       <div>
//                                       <span class="" data-i18n="">{{ issue.key }}</span><br>
//                                       <span class="" data-i18n="">{{ issue.fields.summary }}</span>
//                                       </div>
//                                       <div>
//                                       <span class="" data-i18n="">{{ issue.fields.issuetype }}</span><br>
//                                       <span class="" data-i18n="">{{ issue.fields.status }}</span>
//                                       <span class="dis-none" data-i18n="">{{ issue.fields.description }}</span>
//                                       <span class="dis-none" data-i18n="">{{ issue.fields.created }}</span>
//                                       <span class="dis-none" data-i18n="">{{ issue.fields.creator }}</span>
//                                       </div>
//                                   </a>
//                               </li>