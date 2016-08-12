// Set nav buttons to active on click
$('.nav li').click(function (e) {
    $('.nav li.active').removeClass('active');
    var me = $(this);
    if (!me.hasClass('active')) {
        me.addClass('active');
    }
});

var plexdb = {};

plexdb.toggle_tables = function (element) {
    var e = $(element).parents('.tabledata');
    $('.tabledata').addClass('hidden');
    if (e.hasClass('hidden')) {
        e.removeClass('hidden');
    }
};

plexdb.loadDataTable = function (element, url) {
    var datatable = $(element).dataTable().api();
    plexdb.toggle_tables(element);
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