var plan = 0;
var benefit = 'EMPLOYER';

var toggle_filter = 0;
var industries = ['*'];
var regions = ['*'];
var head_counts = [];
var others = [];

var industries_label = [];
var regions_label = [];
var head_counts_label = [];
var others_label = [];

$(document).ready(function(){
    load_employers();
});

function refresh_content() {
    get_filters();
    $("#data-table-employer").bootgrid('reload');    
}

function load_employers() {
    $("#data-table-employer").bootgrid({
        css: {
            icon: 'zmdi icon',
            iconColumns: 'zmdi-view-module',
            iconDown: 'zmdi-expand-more',
            iconRefresh: 'zmdi-refresh',
            iconUp: 'zmdi-expand-less'
        },
        formatters: {
            "newline": function (column, row) {
                return row[column.id].replace(/@/g, '<br>');
            },
            "commands": function(column, row) {
                return "<button type=\"button\" class=\"btn btn-icon command-eye waves-effect waves-circle\" data-row-id=\"" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></button> " + 
                    "<button type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" data-row-id=\"" + row.id + "\"><span class=\"zmdi zmdi-edit\"></span></button>" + 
                    "<button type=\"button\" class=\"btn btn-icon command-print waves-effect waves-circle\" data-row-id=\"" + row.id + "\"><span class=\"zmdi zmdi-print\"></span></button>";
            }

        },
        templates: {
            footer: "",
            header: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        labels: {
            infos: 'Showing {{ctx.start}} to {{ctx.end}} of {{ctx.total}} Employers',
            noResults: EMPLOYER_THRESHOLD_MESSAGE
        },
        rowCount: [25],
        ajaxSettings: {
            method: "POST",
            cache: false
        },
        requestHandler: function (request) {
            var model = {
                current: request.current,
                rowCount: request.rowCount,
                industry_: industries,
                head_counts: head_counts,
                others: others,
                regions: regions,
                threshold: 0
            };

            return JSON.stringify(model);
        }                
    });        
}    