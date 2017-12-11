function search() {
  $('#searchresults').remove();
  $('#results').append('<div id="searchresults"></div>');

  var phrase = document.getElementById("searchbox").value;
  var choices = phrase.split('is it ').slice(1);

  if (phrase !== "") {
    console.log(phrase);
    console.log(choices);
    $.ajax({
        //url: `https://hq-cheater.herokuapp.com/google?search=${phrase}&choices=${choices}`,
      url: `http://localhost:9000/google?search=${phrase}&choices=${choices}`,
        success: function(response) {
          console.log(response);
					var res = $.parseJSON(response);
					$.each(res, function(k, v) {
            var calculate = v * 10;
            $('#searchresults').append('<h1 class="answer">'+k+'</h1>')
            $('#searchresults').append('<div class="progress"><div class="progress-bar" role="progressbar" style="width: '+calculate+'%" aria-valuenow="'+calculate+'" aria-valuemin="0" aria-valuemax="100"></div></div>');
          });
        }
    })
  }
}
