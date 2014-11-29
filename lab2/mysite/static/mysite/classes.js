function FreeDate(date, h_to, h_from, room) {
    var regexp = /^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/;
    console.log(date);
    if(!date.match(regexp)) throw 'Bad date format';
    hours = [];
    for (i = h_from; i < h_to; i++)
        hours.push(i);
    console.log(h_to, h_from, hours);
    if (Number(h_to) == Number(h_from)) throw 'Bad hours type';
    $.each(hours, function(h) {
        if( isNaN(hours[h]) || Number(hours[h])<=0 || Number(hours[h]>=24) ) throw 'Bad hours type';
    });

    this.date = date;
    this.hours = hours.slice(0);
    this.room = room;
    this.from = h_from;
    this.to = h_to;
    console.log("FreeDate " + this.date + this.hours + this.room);
}

function Attribute(id, name) {
    console.log("attribute name " + name);
    if (typeof(name) != 'string') throw 'Bad type of attribute name';
    this.id = id;
    this.name = name;
}

function Room(id, name, desc, cap, attrs) {

    if (typeof(id) != 'number') throw 'Bad type of room id';
    if (typeof(name) != 'string') throw 'Bad type of room name';
    if (typeof(desc) != 'string') throw 'Bad type of room description';
    if (typeof(cap) != 'number') throw 'Bad type of room capacity';

    this.id = id;
    this.name = name;
    this.description = desc;
    this.capacity = cap;
    //this.freedates = dates;
    this.attributes = attrs;

    // var t_attrs = this.attributes;
    // var t_dates = this.freedates;

    // $.each(dates, function (t) {
    //     var free = new FreeDate(f, dates[t]);
    //     t_dates.push(free);
    // });

    // $.each(attrs, function (a) {
    //     var attr = new Attribute(attrs[a]);
    //     t_attrs.push(attr);
    // });
}