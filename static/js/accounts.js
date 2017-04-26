$(document).ready(function(){
    load_employers();
});

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
            "link": function (column, row) {
                return "<a href=\"/accounts/"+row.id+"\">"+row[column.id]+"</a>";
                // return "<a href=\"/admin/general/employer/"+row.id+"/change\">"+row[column.id]+"</a>";
            },            
            "commands": function(column, row) {
                return "<button type=\"button\" class=\"btn btn-icon command-eye waves-effect waves-circle\" data-row-id=\"" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></button> " + 
                    "<button type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" data-row-id=\"" + row.id + "\"><span class=\"zmdi zmdi-edit\"></span></button>";
            }
        },
        labels: {
            infos: 'Showing {{ctx.start}} to {{ctx.end}} of {{ctx.total}} Employers',
            noResults: EMPLOYER_THRESHOLD_MESSAGE
        },
        ajaxSettings: {
            method: "POST",
            cache: false
        },
        requestHandler: function (request) {
            var model = {
                current: request.current,
                rowCount: request.rowCount,
                q: request.searchPhrase,
                industry_: ['*'],
                head_counts: [],
                others: [],
                regions: ['*'],
                threshold: 0
            };

            return JSON.stringify(model);
        }                
    });       
}