var industries = [];
var head_counts = [];
var others = [];
var regions = [];


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
            "newline": function (column, row) {
                return row[column.id].replace(/@/g, '<br>');
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
            get_fiters();

            var model = {
                current: request.current,
                rowCount: request.rowCount,
                industry_: industries,
                head_counts: head_counts,
                others: others,
                regions: regions
            };

            return JSON.stringify(model);
        }                
    });        
}    


function get_fiters() {
    industries = [];
    head_counts = [];
    others = [];
    regions = [];

    $('#industries :selected').each(function() {
        industries.push($(this).val());
    });

    $('#head-counts :selected').each(function() {
        head_counts.push($(this).val());
    });   

    $('.other_filter:checked').each(function() {
        others.push($(this).val());
    });   

    $('#regions :selected').each(function() {
        regions.push($(this).val());
    });   
}

function get_body() {
    benefit = $('.enterprise-navbar li.active a').html();
    get_fiters();

    $.post(
        '/_enterprise',
        {
            industry: industries,
            head_counts: head_counts,
            benefit: benefit,
            others: others,
            regions: regions
        },
        function(data) {
            $('#bnchmrk_card').html(data);
            if(benefit == 'EMPLOYERS') {
                load_employers();
                // $("#data-table-employer").bootgrid('reload');        
            } else if(benefit == 'LIFE') {
                draw_easy_pie_chart();
                draw_donut_chart('L-1', l1_data);
                draw_bar_chart('L-5', l5_data);                
            }
        })

    $.post(
        '/get_num_employers',
        {
            industry: industries,
            head_counts: head_counts,
            benefit: benefit,
            others: others,
            regions: regions
        },
        function(data) {
            $('#num_employers').html(data);
        })

}

$(document).ready(function(){
    $('.enterprise-navbar li').each(function() {
        if (benefit == $(this).find('a').html()) {
            $(this).addClass('active');
        }
    });

    get_body();

    $('.enterprise-navbar li').click(function() {
        $('.enterprise-navbar li').removeClass('active');
        $(this).addClass('active');
        get_body();
    });

    // $('#industries option:first').attr('selected', 'selected');
    // $('#head-counts option:first').attr('selected', true);
    // $('#regions option:first').attr('selected', true);
});
