function favorite(ID) {
    $.getJSON('/favorite/add', {
        id: ID
    }, function(data) {
        console.log(data)
        if ($("#Fav_" + ID).hasClass("far")) {
            $("#Fav_" + ID).removeClass("far")
            $("#Fav_" + ID).addClass("fas")
        }
        else {
            $("#Fav_" + ID).addClass("far")
            $("#Fav_" + ID).removeClass("fas")
        }
    });
}