// Return a default value for optional arguments
function defaultFor(arg, val) {
    return typeof arg !== 'undefined' ? arg : val;
}

// Add custom sort for data like "x of y"
$.fn.dataTable.ext.type.order['xofy-pre'] = function (data) {
    if (typeof(data) === 'string') {
        return parseInt(data.split(' of ')[0]);
    } else {
        return data;
    }
};
$.fn.dataTable.ext.type.order['views-pre'] = function (data) {
    if (typeof(data) === 'string') {
        return 0;
    } else {
        return data;
    }
};
$.fn.dataTable.ext.type.order['percent-pre'] = function (data) {
    if (typeof(data) === 'string') {
        var start = data.indexOf('width:') + 6;
        var stop = data.indexOf('%') - start;
        return parseInt(data.substr(start, stop));
    } else {
        return data;
    }
};

// PlexDB Namespace
var plexdb = {};

plexdb.navSelector = function (id) {
    $('.nav li.active').removeClass("active");
    $('#' + id).addClass('active');
}

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

plexdb.initDataTable = function (element, url, columns, order) {
    defaultFor(order, [[0, 'asc']]);

    $(element).DataTable({
        ajax: {
            url: url,
            dataSrc: '',
            type: 'GET'
        },
        order: order,
        autoWidth: false,
        lengthMenu: [10, 15, 20, 25, 50, 75, 100],
        columns: columns,
        columnDefs: [
            {type: 'xofy', targets: 'xofy'},
            {
                type: 'title',
                targets: 'title',
                render: function (data, type, full, meta) {
                    return '<a href="#">' + data + '</a>';
                }
            },
            {
                type: 'date',
                targets: 'date',
                render: function (data, type, full, meta) {
                    if (data)
                        return data.substr(0, data.indexOf(' '));
                    else
                        return data;
                }
            },
            {
                type: 'views',
                targets: 'views',
                render: function (data, type, full, meta) {
                    if (data === 0) {
                        return 'incomplete';
                    } else {
                        return data;
                    }
                }
            },
            {
                type: 'percent',
                targets: 'percent',
                render: function (data, type, full, meta) {
                    var percentage = 100;
                    if (typeof(data) === 'number' && data) {
                        percentage = (data / full.duration) * 100;
                    }
                    percentage = Math.round(percentage);
                    if (full.view_count > 0) {
                        percentage = 100;
                    }
                    if (full.view_count === 0 && percentage >= 100) {
                        percentage = 0;
                    }
                    return '' +
                        '<div class="progress">' +
                        '<div class="progress-bar" aria-valuemin="0" aria-valuemax="100"' +
                        ' style="width:' + percentage + '%">' +
                            percentage +
                        '</div></div>';
                }
            }
        ]
    });
};

plexdb.nav_click = function (id, table_id, api_path) {
    plexdb.navSelector(id);
    plexdb.loadDataTable(table_id, api_path);
}
