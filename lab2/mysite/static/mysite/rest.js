$(document).ready(function () {

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

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            $(".modal-body").hide();
            $("#loading_indicator").show();
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        complete:function(){
            $("#loading_indicator").fadeOut();
            $(".modal-body").fadeIn();
            $(".selectable").selectable({
                filter: ".enabled"
            });
            $(".date").click(function(event) {
                $(".ui-state-default").removeClass('ui-selected');
            });
        }
    });

    $('.trhref').click(function() {
        id = $(this).attr('id');
        $.ajax({
            type: 'GET',
            url: 'room_details',
            data: {
                'room_id': id
            },            data: {
                'room_id': id
            },
            dataType: 'json'
        })
        .done(function(data, id){
            $('#myModal').modal('show');
            collapsed_dates = '';
            //gównoJS
            $.each(data.dates, function(entry) {
                table = '';
                for (var i=6; i<30; i++) {
                    table += '<li class="ui-state-default" id="'+ entry + '-' + i%24 + '">' + i%24 + ':00' + '</li>';
                }
                collapsed_dates += '<div class="panel panel-default">'
                                   +'<div class="panel-heading">'
                                   +'<h4 class="panel-title">'
                                   +'<a class="date" data-toggle="collapse" data-parent="#accordion" href="#' + entry + '">'
                                   + entry + ' ----- ' + data.ranges[entry]
                                   +'</a></h4></div><div id="' + entry + '" class="panel-collapse collapse">'
                                   +'<div class="panel-body">'
                                   +'<ol id="selectable" class="selectable">'
                                   +table
                                   +'</ol>'
                                   +'</div></div></div>'
            });
            if (!collapsed_dates) collapsed_dates = "<h1>There is no free terms, sorry.</h1>";
            $('#accordion').html(collapsed_dates);
            $('#room_name').html(data.name);
            $('#room_description').html(data.description);
            $('#room_capacity').html(data.capacity);
            $.each(data.dates, function(entry) {
                $.each(data.dates[entry], function(hour) {
                    $("#" + entry + '-' + data.dates[entry][hour].replace(/^[0]+/g,"")).addClass('enabled');
                });
            });
        });
    });

    $(".adv").click(function (event) {
        $('.primary-search').fadeOut();
    });

    $(".smpl").click(function (event) {
        $('.primary-search').fadeIn();
    });
});