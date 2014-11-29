test("Room", function() {
    var a = Room(1,'nazwa','opis',15,[],[]);
    ok( true, "Correct attribute." );
    throws( function() { Room('www','nazwa','opis',15,[],[]) }, "Bad type of room id" );
    throws( function() { Room(1,123,'opis',15,[],[]) },      "Bad type of room name" );
    throws( function() { Room(1,'nazwa',123,15,[],[]) }, "Bad type of room description" );
    throws( function() { Room(1,'nazwa','opis','www',[],[]) }, "Bad type of room capacity" );
});
test("Attribute", function() {
    var a = Attribute(1, 'nazwa');
    ok( true, "Correct attribute." );
    throws( function() { Attribute(1234, 123) }, "Bad type of attribute type" );
});
test("FreeDate", function() {
    var a = FreeDate('2014-02-01', 12,16, 3);
    ok( true, "Correct attribute." );
    throws( function() { FreeDate('2014-02-01', '12', '12','asdf') }, "Bad hours type" );
    throws( function() { FreeDate('20148-02-01', '12','15','16') }, "Bad date format" );
})