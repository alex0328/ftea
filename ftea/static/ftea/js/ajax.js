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




// translator main function
    $('#pol, #eng').blur(function () {
        if ($(this).val()) {
            let lang = "eng";
            let request_type = "translator";
            if ($(this).attr('name') == "Word_pol") {
                lang = "pol";
            }
            let data = {
                'word': $(this).val(),
                'lang': lang,
                'request_type': request_type
            };
            $.ajax({
                type: "GET",
                url: "/translator/",
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                scriptCharset: "utf-8",
                data: data,
                success: function (resp) {
                    set_values(resp)
                },
                error: function (data) {
                    alert("Sorry, smth goes wrong");
                }
            });
        }
    });
});

// setting values on translator
    function set_values(django_response) {
        console.log(django_response);
        let lang = django_response['lang'];
        let inner = django_response['word']
        if (lang == "pl") {
            $('#pol').val(inner)
        }
        else if (lang == "en"){
            $('#eng').val(inner)
        }
        else {
            $('#error_mess').html("sorry, smth goes wrong")
        }
    }


// delete record from translator database
listener = $('.table_tr a');
    delete_record(listener);

    function delete_record(listener) {
    listener.click(function (event) {
        event.preventDefault();
        let link_value = ($(this).attr('value'));
        let link_obj = $(this);
        let data_to_delete = {
            "id": link_value,
            "request_type": "delete_record"
        };
        $.ajax({
            type: "GET",
            url: "/translator/",
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            scriptCharset: "utf-8",
            data: data_to_delete,
            success: function (resp) {
                console.log(resp['status']);
                if (resp['status'] === 200) {
                    console.log(link_obj.parent().parent().fadeOut());
                }
            },
            error: function (data) {
                alert("Sorry, smth goes wrong");
            }
        });
    });
}


$('#add_to_db').click(function(event) {
    event.preventDefault();
   console.log("działam");
   let word_pol = $('#pol').val();
   let word_eng = $('#eng').val();
   let data_for_db = {"dupa": "kamieni kupa"};
    if (word_pol && word_eng) {
        data_for_db = {"request_type": "add_to_db",
                        "word_eng": word_eng,
                        "word_pol": word_pol};
    $.ajax({
        type: "GET",
        url: "/translator/",
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        scriptCharset: "utf-8",
        data: data_for_db,
        success: function (resp, textStatus, xhr) {
            if (xhr.status === 200) {
                if (resp["new_id"] == "already_exist") {
                    error_message()
                } else {
                    build_tr(resp);
                }
            }
        },
        error: function (data) {
            alert("Sorry, smth goes wrong");
        }
    })
    }

});

    function build_tr(resp) {
        let id_new_word = resp["new_id"],
            en_new = resp["en"],
            pl_new = resp["pl"],
            new_tr = `<tr id=${id_new_word} class="table_tr">
                        <th scope="row">${id_new_word}</th>
                        <td>${en_new}</td>
                        <td>${pl_new}</td>
                        <td><a href="#" value=${id_new_word}>Delete</a></td>
                       </tr>`;
            $('tbody').prepend(new_tr);
    }

    function error_message() {
        $("#error_mess").html("This value already exist");
    }