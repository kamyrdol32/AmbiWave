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

function clipcopy() {
    var copyText = document.getElementById("shareid");
    var changeIcon = document.getElementById("cp");
    copyText.select();
    copyText.setSelectionRange(0, 99999)
    document.execCommand("copy");
    changeIcon.classList.remove('fa-copy');
    changeIcon.classList.add('fa-check');
}