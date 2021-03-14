function player_change(song)
    {
     document.getElementById("player").pause();
     document.getElementById("player").setAttribute('src', song);
     document.getElementById("player").load();
     document.getElementById("player").play();
    }
