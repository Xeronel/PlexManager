var requests = {};
requests.last_search_time = Date.now();
requests.last_search = '';
requests.search_func = requests.search_show;

requests.add_show = function(obj) {
    var search_results = $('#search_results');
    search_results.append(
        '<div class="row content-data">' +
        '<img src="' + obj.show.image.medium + '" class="poster col-lg-4 col-md-4 col-sm-4 col-xs-4">' +
        '<div class="content-info col-lg-8 col-md-8 col-sm-8 col-xs-8"><a href="' + obj.show.url + '">' + obj.show.name + ' (' + obj.show.premiered.split('-')[0] + ')' + '</a>' +
        '<span class="row description col-lg-12 col-md-12 col-sm-12 col-xs-12">' + obj.show.summary + '</span></div>' +
        '</div><hr>'
    )
};

requests.search_show = function (show_name) {
  // Get show
  $.get('http://api.tvmaze.com/search/shows?q=' + show_name, function (data) {
      // Clear search_results
      $('#search_results').html('');
      // Add each show to output
      $(data).each(function (idx, obj) {
          if (obj.show.image) {
              requests.add_show(obj);
          }
      });
  });
}

requests.add_movie = function(obj) {
    $('#search_results').append(
        '<div class="row content-data">' +
        '<img src="https://image.tmdb.org/t/p/w150/' + obj.poster_path + '" class="poster col-lg-4 col-md-4 col-sm-4 col-xs-4">' +
        '<div class="content-info col-lg-8 col-md-8 col-sm-8 col-xs-8"><a href="https://www.themoviedb.org/movie/' + obj.id + '">' + obj.title + ' (' + obj.release_date.split('-')[0] + ')' + '</a>' +
        '<span class="row description col-lg-12 col-md-12 col-sm-12 col-xs-12">' + obj.overview + '</span></div>' +
        '</div><hr>'
    )
};

requests.search_movie = function(movie_name) {
  $.get('https://api.themoviedb.org/3/search/movie?api_key=146285a857bd0e2e19974450468dd5d7&query=' + movie_name, function (data) {
      $('#search_results').html('');
      $(data.results).each(function (idx, obj) {
          if (obj.poster_path) {
              requests.add_movie(obj);
          }
      });
  });
}

requests.search = function (e) {
    if (Date.now() - requests.last_search_time > 500
        && e.value !== requests.last_search
        && e.value !== '') {
        requests.last_search = e.value;
        requests.last_search_time = Date.now();
        requests.search_func(e.value);
        return true;
    } else {
        setTimeout(function () {
            requests.search_func(e.value);
        }, 500);
        return false;
    }
};

$('#tv_button').click(function () {
    $('#tv_button').addClass('active');
    $('#movies_button').removeClass('active');
    requests.search_func = requests.search_show;
    requests.search({value: $('#search').val()});
});

$('#movies_button').click(function () {
    $('#movies_button').addClass('active');
    $('#tv_button').removeClass('active');
    requests.search_func = requests.search_movie;
    requests.search({value: $('#search').val()});
});

$('#search').keyup(function () {
  var result = requests.search(this);
  if (result) {
    console.log("Fired late.");
  }
});
