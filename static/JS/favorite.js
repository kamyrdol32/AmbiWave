function favorite(ID) {
    $.getJSON('/favorite/add', {
        id: ID
      }, function(data) {
        console.log(data)
      });
}