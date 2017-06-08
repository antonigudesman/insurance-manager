var industries = [];
var regions = [];
var head_counts = [];
var others = [];
var states = [];
var industries_label = [];
var head_counts_label = [];
var others_label = [];
var regions_label = [];
var states_label = [];

$(document).ready(function(){
    load_employers();
});

function refresh_content() {
    get_filters();
    get_filters_label();
    $("#data-table-employer").bootgrid('reload');    
}

function load_employers() {
    var grid = $("#data-table-employer").bootgrid({
        css: {
            icon: 'zmdi icon',
            iconColumns: 'zmdi-view-module',
            iconDown: 'zmdi-expand-more',
            iconRefresh: 'zmdi-refresh',
            iconUp: 'zmdi-expand-less'
        },
        formatters: {
            "link": function (column, row) {
                return "<a target='_self' href=\"/accounts/"+row.id+"\">"+row[column.id]+"</a>";
                // return "<a href=\"/admin/general/employer/"+row.id+"/change\">"+row[column.id]+"</a>";
            },            
            "commands": function(column, row) {
                return "<button type=\"button\" class=\"btn btn-icon command-print waves-effect waves-circle\" data-row-id=\"" + row.id + "\"><span class=\"zmdi zmdi-print\"></span></button> ";
            }
        },
        labels: {
            infos: 'Showing {{ctx.start}} to {{ctx.end}} of {{ctx.total}} Employers',
            noResults: 'No Employers Found'
        },
        ajaxSettings: {
            method: "POST",
            cache: false
        },
        requestHandler: function (request) {
            var model = {
                current: request.current,
                rowCount: request.rowCount,
                industry_: industries,
                q: request.searchPhrase,
                head_counts: head_counts,
                others: others,
                regions: regions,
                states: states,
                threshold: 0,

                print: true,
                industry_label: industries_label,
                head_counts_label: head_counts_label,
                others_label: others_label,
                regions_label: regions_label,
                states_label: states_label,                
            };

            return JSON.stringify(model);
        }                
    }).on("loaded.rs.jquery.bootgrid", function() {
        grid.find(".command-print").on("click", function(e) {
            var myWindow = window.open("/print_plan_order/"+$(this).data("row-id"), "myWindow"+$(this).data("row-id"), "width=1000,height=600,left=200,top=200,scrollbars=yes,status=1");
        });
    });       
}