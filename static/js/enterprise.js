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

var colors = ['#f8696b', '#FCAA78', '#bfbfbf', '#B1D480', '#63be7b'];

$(document).ready(function(){
    if (print_template) {
        update_properties();
        update_content(benefit);
    } else {
        $('.enterprise-navbar li').each(function() {
            if (benefit == $(this).find('a').html()) {
                $(this).addClass('active');
            }
        });

        get_body();

        // change benefit
        $('.enterprise-navbar li').click(function() {
            $('.enterprise-navbar li').removeClass('active');
            $(this).addClass('active');
            plan = -2;
            get_body();
        });

        // toggle filters
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
    if (!print_template) 
        if (plan != -2) // not changed benefit
            plan = $('#plans').val();
        else
            plan = 0;
    else
        plan = -1;

    $.post(
        '/update_properties',
        {
            benefit: benefit,
            plan: plan
        },
        function(data) {
            $.each(data, function( key, value ) {
                if (key.match("^rank_")) {
                    $('#prop_'+key).html(value);
                    $('#prop_'+key).removeAttr('style');
                    if ( value != 'N/A' ) {
                        $('#prop_'+key).css('color', colors[value-1]);
                    }
                } else {
                    $('#prop_'+key).html(value);
                }
            });            
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
    $('.page-loader').show();
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

            update_content(benefit);
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

generate_quintile_data = function(raw_data, inverse){
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
        var color_index = inverse ? 5 - raw_data[i][0] / 20 : raw_data[i][0] / 20 - 1;
        section.push(raw_data[i]);
        if ( i > 0 && raw_data[i][0] % 20 == 0) {
            data.push({
                data : section,
                points: { show: false },
                lines: { show: true, fill: 0.98 },
                color: colors[color_index]
            });
            section = [raw_data[i]];
        }
    }       
    return data;
}

update_content = function(benefit) {
    if(benefit == 'EMPLOYERS') {
        load_employers();
    } else if ($.inArray(benefit, ["LIFE", "STD", "LTD"]) != -1) {
        gh1_data = generate_quintile_data(gh1_data);

        if ( benefit == "LTD")
            gh2_data = generate_quintile_data(gh2_data, true);
        else
            gh2_data = generate_quintile_data(gh2_data);
        
        draw_bar_chart(benefit+'-1', gh1_data);        
        
        if ( benefit == "LIFE")
            draw_bar_chart(benefit+'-2', gh2_data);        
        else
            draw_bar_chart(benefit+'-2', gh2_data, true, 7);        
      
        draw_easy_pie_chart();
        draw_donut_chart(benefit+'-18', gh18_data);
    } else if ($.inArray(benefit, ["STRATEGY"]) != -1) {
        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, true);
        
        draw_bar_chart(benefit+'-1', gh1_data);        
        draw_bar_chart(benefit+'-2', gh2_data);        
    } else if ($.inArray(benefit, ["VISION"]) != -1) {
        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, true);
        gh3_data = generate_quintile_data(gh3_data);
        gh4_data = generate_quintile_data(gh4_data);
        gh5_data = generate_quintile_data(gh5_data, true);
        gh6_data = generate_quintile_data(gh6_data, true);        
        
        draw_bar_chart(benefit+'-1', gh1_data, false, 7);        
        draw_bar_chart(benefit+'-2', gh2_data, false, 7);        
        draw_bar_chart(benefit+'-3', gh3_data, false, 7);        
        draw_bar_chart(benefit+'-4', gh4_data, false, 7);        
        draw_bar_chart(benefit+'-5', gh5_data, false, 7);        
        draw_bar_chart(benefit+'-6', gh6_data, false, 7);        

        draw_donut_chart(benefit+'-18', gh18_data);
    } else if ($.inArray(benefit, ["DPPO", "DMO"]) != -1) {
        if (benefit == "DMO")
            $('.out-benefit').remove();

        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data);
        gh3_data = generate_quintile_data(gh3_data, true);
        gh4_data = generate_quintile_data(gh4_data);
        gh5_data = generate_quintile_data(gh5_data, true);
        gh6_data = generate_quintile_data(gh6_data, true);
        gh7_data = generate_quintile_data(gh7_data, true);
        gh8_data = generate_quintile_data(gh8_data, true);
        gh9_data = generate_quintile_data(gh9_data, true);
        gh10_data = generate_quintile_data(gh10_data, true);        
        
        draw_bar_chart('DENTAL-1', gh1_data, false, 7);        
        draw_bar_chart('DENTAL-2', gh2_data, false, 7);        
        draw_bar_chart('DENTAL-3', gh3_data, false, 7);        
        draw_bar_chart('DENTAL-4', gh4_data, false, 7);        
        draw_bar_chart('DENTAL-5', gh5_data, false, 7);        
        draw_bar_chart('DENTAL-6', gh6_data, false, 7);        
        draw_bar_chart('DENTAL-7', gh7_data, false, 7);        
        draw_bar_chart('DENTAL-8', gh8_data, false, 7);        
        draw_bar_chart('DENTAL-9', gh9_data, false, 7);        
        draw_bar_chart('DENTAL-10', gh10_data, false, 7);        

        draw_donut_chart('DENTAL-18', gh18_data);
    } else if ($.inArray(benefit, ["PPO", "HMO", "HDHP"]) != -1) {
        if (benefit == "HMO")
            $('.out-benefit').remove();
        else if (benefit == 'HDHP')
            $('.hdhp-benefit').remove();
        else
            $('.ppo-benefit').remove();

        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, true);
        gh3_data = generate_quintile_data(gh3_data, true);
        gh4_data = generate_quintile_data(gh4_data, true);
        gh5_data = generate_quintile_data(gh5_data, true);
        gh6_data = generate_quintile_data(gh6_data, true);
        gh7_data = generate_quintile_data(gh7_data, true);
        gh8_data = generate_quintile_data(gh8_data, true);
        gh9_data = generate_quintile_data(gh9_data, true);
        gh10_data = generate_quintile_data(gh10_data, true);        
        gh11_data = generate_quintile_data(gh11_data, true);
        gh12_data = generate_quintile_data(gh12_data, true);
        gh13_data = generate_quintile_data(gh13_data, true);
        gh14_data = generate_quintile_data(gh14_data, true);
        gh15_data = generate_quintile_data(gh15_data, true);
        gh16_data = generate_quintile_data(gh16_data, true);
        gh17_data = generate_quintile_data(gh17_data, true);
        gh19_data = generate_quintile_data(gh19_data, true);
        gh20_data = generate_quintile_data(gh20_data, true);        
        gh21_data = generate_quintile_data(gh21_data, true);        
        gh22_data = generate_quintile_data(gh22_data);
        
        draw_bar_chart('MEDICAL-1', gh1_data, false, 7);        
        draw_bar_chart('MEDICAL-2', gh2_data, false, 7);        
        draw_bar_chart('MEDICAL-3', gh3_data, false, 7);        
        draw_bar_chart('MEDICAL-4', gh4_data, false, 7);        
        draw_bar_chart('MEDICAL-5', gh5_data, false, 7);        
        draw_bar_chart('MEDICAL-6', gh6_data, false, 7);        
        draw_bar_chart('MEDICAL-7', gh7_data, false, 7);        
        draw_bar_chart('MEDICAL-8', gh8_data, false, 7);        
        draw_bar_chart('MEDICAL-9', gh9_data, false, 7);        
        draw_bar_chart('MEDICAL-10', gh10_data, false, 7);        
        draw_bar_chart('MEDICAL-11', gh11_data, false, 7);        
        draw_bar_chart('MEDICAL-12', gh12_data, false, 7);        
        draw_bar_chart('MEDICAL-13', gh13_data, false, 7);        
        draw_bar_chart('MEDICAL-14', gh14_data, false, 7);        
        draw_bar_chart('MEDICAL-15', gh15_data, false, 7);        
        draw_bar_chart('MEDICAL-16', gh16_data, false, 7);        
        draw_bar_chart('MEDICAL-17', gh17_data, false, 7);        
        draw_bar_chart('MEDICAL-19', gh19_data, false, 7);        
        draw_bar_chart('MEDICAL-20', gh20_data, false, 7);   
        draw_bar_chart('MEDICAL-21', gh21_data, false, 7);        
        draw_bar_chart('MEDICAL-22', gh22_data, false, 7);   

        draw_donut_chart('MEDICAL-18', gh18_data);
    }

    $('.page-loader').fadeOut();
}