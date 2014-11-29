
$(document).ready(function () {


    console.log("offline.js");

    var id;
    var rooms = [];
    var attributes = [];
    var freedates = [];
    var act_rooms = [];
    var sorted_by_name = false;
    var sorted_by_capacity = false;
    var page = 1;
    var free_dict = new Object();
    var sort_row = '<tr id="sort-panel"><td><a id="sort-name">Name</a>'
                   +'</td><td class="text-center"><a id="descp">Description</a>'
                   +'</td><td class="text-center"><a id="sort-cap">Catacity</a></td></tr>';

    function sortByName() {
        console.log("sortbyname");
        if (!sorted_by_name) {
            act_rooms.sort(function(a,b){
                if(a.name < b.name) return -1;
                if(a.name > b.name) return 1;
                return 0;
            });
            sorted_by_name = true;
        } else {
            act_rooms.sort(function(a,b){
                if(a.name > b.name) return -1;
                if(a.name < b.name) return 1;
                return 0;
            });
            sorted_by_name = false;
        }
        makeRoomList(act_rooms);
    }

    function sortByCapacity() {
        console.log("sortByCapacity");
        if (!sorted_by_capacity) {
            act_rooms.sort(function(a,b){
                return (a.capacity - b.capacity);
            });
            sorted_by_capacity = true;
        } else {
            act_rooms.sort(function(a,b){
                return (b.capacity - a.capacity);
            });
            sorted_by_capacity = false;
        }
        makeRoomList(act_rooms);
    }

    function simpleSearch() {
        var query = $("#zapytanie").val();
        console.log("simpleSearch " + query);
        var queryset = [];
        $.each(rooms, function(r) {
            if(rooms[r].name.indexOf(query) >= 0) {
                queryset.push(rooms[r]);
            }
        });
        page = 1;
        act_rooms = queryset;
        makeRoomList(act_rooms);
    }

    function advancedSearch() {
        console.log("advancedSearch");
        var description = $("#description").val();
        var min = $("#min").val();
        var max = $("#max").val();
        var name = $("#name").val();

        var queryset = [];

        console.log(name + " " + description + " " + min + " " + max + " " + queryset);

        $.each(rooms, function(r) {
            match = true;
            if ($("#attributs :checked").length > 0) {
                console.log("zaznaczone jakies atrybuty,");
                $("#attributs :checked").each(function () {
                    attr = $(this).text();
                    found = false;
                    for (var i = 0; i < rooms[r].attributes.length; i++) {
                       // var attrNum = attributesrooms[r].attributes[i];
                        for (var j = 0; j < attributes.length; j++) {
                            if (attributes[j].id == rooms[r].attributes[i])
                                if (attributes[j].name == attr) {
                                    found = true; 
                                    break;
                                }

                        }
                        // if (rooms[r].attributes[i].name == attr) found = true;
                        // break;
                    }
                    if (!found) match = false;
                });
            } else {
                match = true;
            }

            if (!(( match ) &&
                (rooms[r].name.indexOf(name) >= 0) &&
                (rooms[r].description.indexOf(description) >= 0)))
                    match = false;

            if (match && min) {
                if (!(rooms[r].capacity >= min)) 
                    match = false;
            }
            if (match && max) {
                if (!(rooms[r].capacity <= max)) 
                    match = false;
            }

            if (match) {
                queryset.push(rooms[r]);
            }
        });

        page = 1;
        act_rooms = queryset;
        makeRoomList(act_rooms);
    }

    function paginate(array) {
        console.log("dlugosc tablicy z pokojami" + array.length);
        array = array.slice(5*(page-1), 5*page);
        return array;
    }

    function createRooms() {
        var data = JSON.parse(JSON.parse(localStorage.getItem("room_list")));
        console.log((JSON.parse(localStorage.getItem("room_list"))));
        console.log("przeszło");
        if(data) {
            console.log("jakies dane" + data[0].fields.name + data[0].pk);
            $.each(data, function (entry) {
                console.log("entry " + entry);
                r = data[entry].fields;
                console.log(r + data[entry].pk);
                var room = new Room(data[entry].pk, r.name, r.description, r.capacity, r.attributes);
                console.log("room " + room.id + room.name);
                rooms.push(room);
            });
            act_rooms = rooms.slice(0);
            createFreeDict();
        }
    }

    function createFreeDict() {
        console.log("freeDates" + freedates[0].room);
        free_dict = new Object();
        for ( i = 0; i < rooms.length; i++) {
            var d = [];
            var t_r = [];
            var r = rooms[i].id;
            for ( j = 0; j < freedates.length; j++) {
                if (freedates[j].room == rooms[i].id) {
                    console.log("room = room" + freedates[j].room + " " + rooms[i].id + " " + freedates[j].hours);
                    d.push(freedates[j]);
                }
            }
            console.log("d + length" + d + freedates.length);
            if (d.length != 0) {
                free_dict[r] = d;
            } 
            else
                free_dict[r] = null;
        }
        
        console.log("free_dict " + i + (free_dict[1] == null));
    }

    function createAttributes() {
        var data = JSON.parse(JSON.parse(localStorage.getItem("attr_list")));
        console.log((JSON.parse(localStorage.getItem("attr_list"))));
        console.log("przeszło");
        var a_list = '';
        if (data) {
            console.log("jakies dane" + data[0].fields.name);
            $.each(data, function (entry) {
                console.log("entry " + entry);
                r = data[entry].fields;
                console.log(r);
                var attr = new Attribute(data[entry].pk, r.name);
                attributes.push(attr);
                a_list += '<option value="';
                a_list += r.name;
                a_list += '">';
                a_list += (r.name + '</option>');
            });
            //console.log(a_list);
            return a_list;
        }
    }

    function createFreeDates() {
        var data = JSON.parse(JSON.parse(localStorage.getItem("free_list")));
        // console.log((JSON.parse(localStorage.getItem("free_list"))));
        // console.log("przeszło");
        if(data) {
            // console.log("jakies dane" + data[0].fields.date);
            $.each(data, function (entry) {
                // console.log("entry " + entry);
                r = data[entry].fields;
                // console.log("freedate" + data[entry].fields.room);
                var free = new FreeDate(r.date, r.to, r.From, r.room);
                freedates.push(free);
            });
        }
    }

    function makeListEntry(room) {
        entry = '<tr id="' + room.id + '" class="trhref"><td>'
                + room.name + '</td><td class="text-center">'
                + room.description + '</td><td class="text-center">'
                + room.capacity + '</td></tr>';
        return entry;
    }

    function updateFreeDates(room) {
        console.log("updateFreeDates");
           $.ajax({
            type: 'GET',
            url: 'get_free_list',
            dataType: 'json'
        })
        .done(function(data) {
            localStorage.setItem("free_list", JSON.stringify(data));
            console.log(JSON.parse(localStorage.getItem("free_list")));
            // console.log(localStorage.getItem("room_list"));
            console.log('done!');
        })
        .fail(function() {
            console.log( "error" );
            })
        .always(function() {
            freedates = [];
            createFreeDates();
        //     makeRoomList(act_rooms);
        });
    }


    function updateRoom(room_id) {
    console.log("updateroom");
           $.ajax({
            type: 'GET',
            url: 'get_free_list',
            dataType: 'json'
        })
        .done(function(data) {
            localStorage.setItem("free_list", JSON.stringify(data));
            console.log(JSON.parse(localStorage.getItem("free_list")));
            // console.log(localStorage.getItem("room_list"));
            console.log('done!');
        })
        .fail(function() {
            console.log( "error" );
            })
        .always(function() {
            freedates = [];
            createFreeDates();
            fillModal(room_id);
        //     makeRoomList(act_rooms);
        });
    }

    function fillModal(room_id) {
        collapsed_dates = '';
        id = room_id;
        // var jqxhr = $.ajax( "formularz", {type:"POST", 
        //     data: {'room_id': id } } )
        // var data = JSON.parse(localStorage.getItem("room_list"));
        // var dates = data[room_id][0].dates;

        var data = free_dict[room_id];
        var number = room_id;
        for ( i = 0; i < rooms.length; i++) {
            if (rooms[i].id == room_id) {
                number = i;
                console.log(number);
                break;
            }
        }
        console.log(number + room_id);
        // var data = JSON.parse(localStorage.getItem("room_list"));
        // var dates = data[room_id][0].terms;
        if (data != null) {
        $.each(data, function(entry) {
            console.log("fill entry" + data[entry].date);
            table = '';
            // for (var i=6; i<30; i++) {
            //     table += '<li class="ui-state-default" id="'+ entry + '-' + i%24 + '">' + i%24 + ':00' + '</li>';
            // }
            var h = data[entry].hours;
            for (var i = 0; i < data[entry].hours.length; i++) {
                   table += '<option value=' + h[i] + ' name = ' + h[i] + ' type="checkbox">' + h[i] + '</option>';
                    //$("#" + entry + '-' + data[entry].hours.i.replace(/^[0]+/g,""));
                }
            collapsed_dates += '<div class="panel panel-default">'
                               +'<div class="panel-heading">'
                               +'<h4 class="panel-title">'
                               +'<a class="date" data-toggle="collapse" data-parent="#accordion" href="#' + entry + '">'
                               + data[entry].date + ' godziny: ' + data[entry].from + ' - ' + data[entry].to
                               +'</a></h4></div><div id="' + entry + '" class="panel-collapse collapse" val=' + data[entry].date + '>'
                               +'<div class="panel-body">'
                               +'<select data-placeholder="Choose hours" class="chosen-select" multiple style="width:350px;" tabindex="16" id="multiple-label" name="multiple-label">'
                               + table
                               +'</select>'
                               +'</div></div></div>'

        });
        }
        if (!collapsed_dates) collapsed_dates = "There are no free dates available. We are sorry. ;(";
        console.log("collapsed_dates" + collapsed_dates);
        $('#accordion').html(collapsed_dates);
        $('#room_name').html(rooms[number].name);
        $('#room_description').html(rooms[number].description);
        $('#room_capacity').html(rooms[number].capacity);
        if (data != null) {
            $.each(data, function(entry) {
                for (var i = 0; i < data[entry].hours.length; i++) {
                     $("#" + entry + '-' + data[entry].hours[i].replace(/^[0]+/g,""));
                }
            });
        }
        console.log( "fillModal" );
        console.log(data);
        if (data != null)
            $(".modal-body").html(data);
    }

    $("#book").click(function(event){
        console.log("book");
        date = $('.collapse').filter('.in').attr('val');
        console.log(date);
        var hours = [];
        if( $('#multiple-label :checked').length > 0){
          //build an array of selected values
          var selectednumbers = [];
          $('#multiple-label :checked').each(function(i, selected) {
              selectednumbers[i] = $(selected).val();
          });
          var json_hours = JSON.stringify(selectednumbers);
          console.log("wybrane, ", JSON.stringify(selectednumbers));
          $.ajax({
                type: 'POST',
                url: 'newReservation',
                data: {
                    'room_id': id,
                    'date': date,
                    'hours': json_hours
                },
                dataType: 'json',
                success: function (data) {
                    console.log("success");
                    if (data["HTTPRESPONSE"] == 1) {
                        $('#myModal').modal('hide');
                        $('#done-alert').html('Done!');
                        $('#done-alert').fadeIn();
                        setTimeout(function () {
                            $('#done-alert').fadeOut();
                        }, 2000);
                    } else {
                        alert(data["ERROR"])
                    }
                }
            })
            .done(function () {
                console.log('Done!');
                updateLocal();
            })
            .fail(function (data) {
                 console.log(data);//["HTTPRESPONSE"]);
                $('#modal-fail-alert').html('No internet connection!');
                $('#modal-fail-alert').fadeIn();
                setTimeout(function () {
                    $('#modal-fail-alert').fadeOut();
                }, 2000);
            });
        }
        else {
            $('#modal-fail-alert').html('You must choose at least one term');
            $('#modal-fail-alert').fadeIn();
            setTimeout(function () {
                $('#modal-fail-alert').fadeOut();
            }, 2000);
        }
    });

    function makeRoomList(array) {
        console.log("makeRoomList");
        array = paginate(array);

        $("#prev-page").attr("disabled", false);
        $("#next-page").attr("disabled", false);
        if (page == 1) $("#prev-page").attr("disabled", true);
        if (page >= Math.ceil(act_rooms.length/5)) $("#next-page").attr("disabled", true);

        var list = '';
        if (array.length == 0) {
           $("#sort-panel").addClass('hidden');
           $("#room-list").html("<tr><td>There are no rooms.</td></tr>");
        } else {
            $("#sort-panel").removeClass('hidden');

            $.each(array, function(entry) {
               list += makeListEntry(array[entry]);
            });
            list = sort_row + list;
            $("#room-list").html(list);
        }
    }

    function updateLocal() {
        console.log("updateLocal");
        // console.log(data);
        $.ajax({
            type: 'GET',
            url: 'get_rooms_list',
            dataType: 'json'
        })
        .done(function(data) {
            localStorage.setItem("room_list", JSON.stringify(data));
            // console.log(localStorage.getItem("room_list"));
            console.log('done!');
        })
        .fail(function() {
            console.log( "error" );
            })
        .always(function() {
            rooms = [];
            createRooms();
            makeRoomList(act_rooms);
        });
    }

    function updateAttr() {
        console.log("updateAttr");
        $.ajax({
            type: 'GET',
            url: 'get_attr_list',
            dataType: 'json'
        })
        .done(function(data) {
            localStorage.setItem("attr_list", JSON.stringify(data));
            // console.log(localStorage.getItem("room_list"));
            console.log('done!');
        })
        .fail(function() {
            console.log( "error" );
            })
        .always(function() {
            attributes = [];
            var x = createAttributes();
            $("#atr").html(x);
           // console.log($("#attributs"));
            // makeRoomList(act_rooms);
        });
    }

    function updateFreeDates() {
        console.log("updateFreeDates");
           $.ajax({
            type: 'GET',
            url: 'get_free_list',
            dataType: 'json'
        })
        .done(function(data) {
            localStorage.setItem("free_list", JSON.stringify(data));
            console.log(JSON.parse(localStorage.getItem("free_list")));
            // console.log(localStorage.getItem("room_list"));
            console.log('done!');
        })
        .fail(function() {
            console.log( "error" );
            })
        .always(function() {
            freedates = [];
            createFreeDates();
        //     makeRoomList(act_rooms);
        });
    }



    $("table").delegate('.trhref', "click", function(e) {
        room_id = $(this).attr('id');
        console.log("klikniete na pokoj" + room_id);
        updateRoom(room_id);
        // $(".selectable").selectable({
        //         filter: ".enabled"
        // });
        // $(".date").click(function(event) {
        //     $(".ui-state-default").removeClass('ui-selected');
        // });
        $('#myModal').modal('show');
    });

    $("table").delegate('#sort-name', "click", function(e) {
        sortByName();
    });
    $("table").delegate('#sort-cap', "click", function(e) {
        sortByCapacity();
    });

    $("#simple-search").click(function () {
       simpleSearch();
    });
    $("#adv-search").click(function () {
       advancedSearch();
    });
    $("#next-page").click(function () {
       if(page < Math.ceil(act_rooms.length/5)) page++;
        console.log(page);
        makeRoomList(act_rooms);
    });
    $("#prev-page").click(function () {
       if(page>1) page--;
        console.log(page);
        makeRoomList(act_rooms);
    });

    updateFreeDates();
    updateAttr();
    updateLocal();
});