var requests = {};
requests.last_search_time = Date.now();
requests.last_search = '';

requests.search_show = function (e) {
    if (Date.now() - requests.last_search_time > 500
        && e.value !== requests.last_search
        && e.value !== '') {
        var value = e.value;
        $.get('http://api.tvmaze.com/search/shows?q=' + value, function (data) {
            var output = $('#output');
            output.html('');
            $(data).each(function (idx, obj) {
                if (obj.show.image) {
                    output.append('<img src="' + obj.show.image.medium + '">');
                    output.append(obj.show.name + '<br>');
                }
            });
        });
        requests.last_search = value;
        requests.last_search_time = Date.now();
        return true;
    } else {
        setTimeout(function () {
            requests.search_show(e);
        }, 500);
        return false;
    }
};

$(function () {
    $('#search').keyup(function () {
        var result = requests.search_show(this);
        if (result) {
            console.log("Fired late.");
        }
    });
});