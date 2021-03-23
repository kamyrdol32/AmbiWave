function like(ID) {
    $.getJSON('/like/add', {
        id: ID
    }, function(data) {
        console.log(data);
        $("#ID_Like").css({"color": "green"});
        location.reload();
    });
}

function unlike(ID) {
    $.getJSON('/unlike/add', {
        id: ID
    }, function(data) {
        console.log(data);
        $("#ID_Dislike").css({"color": "red"});
        location.reload();
    });
}