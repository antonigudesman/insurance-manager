var industries = [];
var head_counts = [];
var others = [];
var regions = [];

var industries_label = [];
var head_counts_label = [];
var others_label = [];
var regions_label = [];

var colors = ['#d52929', '#ebf62f', '#bfbfbf', '#cdd529', '#29d529'];

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

    $('.dropdown-icon').click(function() {
        $('.filter-control').attr('size', 15);
    });    
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
            get_filters();

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

function get_filters() {
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

function get_filters_label() {
    industries_label = [];
    head_counts_label = [];
    others_label = [];
    regions_label = [];

    $('#industries :selected').each(function() {
        industries_label.push($(this).html());
    });

    $('#head-counts :selected').each(function() {
        head_counts_label.push($(this).html());
    });   

    $('.other_filter:checked').each(function() {
        others_label.push($(this).next().html());
    });   

    $('#regions :selected').each(function() {
        regions_label.push($(this).html());
    });   
}

function get_body() {
    $('.filter-control').attr('size', 1);
    benefit = $('.enterprise-navbar li.active a').html();
    get_filters();
    get_filters_label();

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
            } else if(benefit == 'LIFE') {
                draw_bar_chart('L-1', l1_data);        
                draw_bar_chart('L-2', l2_data);        
                draw_easy_pie_chart();
                draw_donut_chart('L-18', l18_data);

                $('#lbl_ft_industries').html(industries_label.toString());
                $('#lbl_ft_regions').html(regions_label.toString());
                $('#lbl_ft_headcounts').html(head_counts_label.toString());
                $('#lbl_ft_other').html(others_label.toString());
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

generate_quintile_data = function(raw_data){
    var qa_points = $.map(raw_data, function(i){if (i[0]%20==0) return [i];});
    var data = [
        {
            data: qa_points,
            points: { show: true, radius: 5 },
            lines: { show: false, fill: 0.98 },
            color: '#f1dd2c'
        }
    ];

    var section = [];
    for( var i = 0; i < raw_data.length; i++ ) {
        section.push(raw_data[i]);
        if ( i > 0 && raw_data[i][0] % 20 == 0) {
            data.push({
                data : section,
                points: { show: false },
                lines: { show: true, fill: 0.98 },
                color: colors[raw_data[i][0] / 20 - 1]
            });
            section = [raw_data[i]];
        }
    }       
    return data;
}