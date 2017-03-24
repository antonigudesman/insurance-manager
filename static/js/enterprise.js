var plan = 0;
var toggle_filter = 0;
var industries = [];
var regions = [];
var head_counts = [];
var others = [];

var industries_label = [];
var regions_label = [];
var head_counts_label = [];
var others_label = [];

var colors = ['#f8696b', '#FCAA78', '#808080', '#B1D480', '#63be7b'];

$(document).ready(function(){
    if (print_template) {
        update_properties();

        l1_data = generate_quintile_data(l1_data);
        l2_data = generate_quintile_data(l2_data);

        draw_bar_chart('L-1', l1_data);        
        draw_bar_chart('L-2', l2_data);        
        draw_easy_pie_chart();
        draw_donut_chart('L-18', l18_data);

    } else {
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

        // expand filters
        $('.dropdown-icon').click(function() {
            toggle_filter = 1 - toggle_filter;
            var f_size = 19 * toggle_filter + 1;
            $('.filter-control').attr('size', f_size);
        });    

        // choose plan
        $('#plans').change(function() {
            update_properties();
        });    

    }
});

function update_properties() {
    plan = -1;
    if (!print_template) 
        plan = $('#plans').val();

    $.post(
        '/update_properties',
        {
            benefit: benefit,
            plan: plan
        },
        function(data) {
            if(benefit == 'LIFE') {
                $('#prop_multiple_max').html(data.multiple_max);
                $('#prop_multiple').html(data.multiple);
                $('#prop_flat_amount').html(data.flat_amount);
                $('#prop_add_flat').html(data.add_flat);
                $('#prop_add_multiple').html(data.add_multiple);
                $('#prop_rank_flat').html(data.rank_flat);
                $('#prop_rank_flat').removeAttr('style');
                if (data.rank_flat != 'N/A')
                    $('#prop_rank_flat').css('color', colors[data.rank_flat-1]);
                $('#prop_rank_multiple').html(data.rank_multiple);
                $('#prop_rank_multiple').removeAttr('style');
                if (data.rank_multiple != 'N/A')
                    $('#prop_rank_multiple').css('color', colors[data.rank_multiple-1]);
            }
        });
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
                regions: regions
            };

            return JSON.stringify(model);
        }                
    });        
}    

function get_filters() {
    industries = [];
    regions = [];
    head_counts = [];
    others = [];

    benefit = $('.enterprise-navbar li.active a').html();    

    $('#industries :selected').each(function() {
        industries.push($(this).val());
    });

    $('#regions :selected').each(function() {
        regions.push($(this).val());
    }); 

    $('#head-counts :selected').each(function() {
        head_counts.push($(this).val());
    });   

    $('#other_filter :selected').each(function() {
        others.push($(this).val());
    });     
}

function get_filters_label() {
    industries_label = [];
    regions_label = [];
    head_counts_label = [];
    others_label = [];

    $('#industries :selected').each(function() {
        industries_label.push($(this).html());
    });

    $('#regions :selected').each(function() {
        regions_label.push($(this).html());
    }); 

    $('#head-counts :selected').each(function() {
        head_counts_label.push($(this).html());
    });   

    $('#other_filter :selected').each(function() {
        others_label.push($(this).html());
    });     

    // for default filters
    if (industries_label.length == 0)
        industries_label.push('All Industries');

    if (regions_label.length == 0)
        regions_label.push('All Regions');

    if (head_counts_label.length == 0)
        head_counts_label.push('All Sizes');

    if (others_label.length == 0)
        others_label.push('Other');

}

// called for only real template
function get_body() {
    // collapse filters
    $('.filter-control').attr('size', 1);

    get_filters();
    get_filters_label();

    $.post(
        '/_enterprise',
        {
            industry: industries,
            head_counts: head_counts,
            others: others,
            regions: regions,

            industry_label: industries_label,
            head_counts_label: head_counts_label,
            others_label: others_label,
            regions_label: regions_label,

            benefit: benefit,
            plan: plan
        },
        function(data) {
            $('#bnchmrk_card').html(data);
            update_properties();

            if ($.inArray(benefit, ["HOME", "TICKET"]) < 0) {
                $('#lbl_ft_industries').html(industries_label.join(', '));
                $('#lbl_ft_regions').html(regions_label.join(', '));
                $('#lbl_ft_headcounts').html(head_counts_label.join(', '));
                $('#lbl_ft_other').html(others_label.join(', '));                
            }

            if(benefit == 'EMPLOYERS') {
                load_employers();
            } else if(benefit == 'LIFE') {
                l1_data = generate_quintile_data(l1_data);
                l2_data = generate_quintile_data(l2_data);
                
                draw_bar_chart('L-1', l1_data);        
                draw_bar_chart('L-2', l2_data);        
                draw_easy_pie_chart();
                draw_donut_chart('L-18', l18_data);
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

    $.post(
        '/get_plans',
        {
            benefit: benefit,
        },
        function(data) {
            $('#plans').html(data);
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

