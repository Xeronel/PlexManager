// Set nav buttons to active on click
$('.nav li').click(function (e) {
    $('.nav li.active').removeClass('active');
    var me = $(this);
    if (!me.hasClass('active')) {
        me.addClass('active');
    }
});

var plexdb = {};

plexdb.toggle_tables = function () {
    var unwatched_table = $('#unwatched_data');
    var watched_table = $('#watched_data');

    if (unwatched_table.hasClass('hidden')) {
        unwatched_table.removeClass('hidden');
    } else {
        unwatched_table.addClass('hidden');
    }

    if (watched_table.hasClass('hidden')) {
        watched_table.removeClass('hidden');
    } else {
        watched_table.addClass('hidden');
    }
};

plexdb.loadDataTable = function (element, url) {
    var datatable = $(element).dataTable().api();
    plexdb.toggle_tables();
    datatable.ajax.url(url).load();
};

plexdb.initDataTable = function (element, url, columns) {
    $(element).DataTable({
        ajax: {
            url: url,
            dataSrc: '',
            type: 'GET'
        },
        autoWidth: false,
        lengthMenu: [10, 15, 20, 25, 50, 75, 100],
        columns: columns
    });
};