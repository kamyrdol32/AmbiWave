function favorite(ID) {
    $.ajax('/favorite/add', {
        id: ID
      }, function(data) {
        console.log(data)
      });
}