var industries = [];
var regions = [];
var head_counts = [];
var others = [];
var states = [];
var plan_type = '';
var plan = 0;

var colors = ['#f8696b', '#FCAA78', '#bfbfbf', '#B1D480', '#63be7b'];

jQuery(function($) {
	// mark left menu selected
    $('ul.stem-menu li').eq(2).addClass('active');

    $('ul.stem-menu li a').removeClass('active');
    $('ul.stem-menu li a').each(function() {
        if ($(this).attr('href').indexOf(bnchmrk_benefit.toLowerCase()) >= 0)
            $(this).addClass('active');
    });

    get_plan_type();

    $('#plans').change(function() {
    	update_properties();
    });
});

function refresh_content() {
    get_body();
}

function get_plan_type() {
    $.get(
        '/get_plan_type',
        {
            bnchmrk_benefit: bnchmrk_benefit,
        },
        function(data) {
            var content = '';
            for(i = 0; i < data.length; i++)
            	content += '<option value="'+data[i]+'">'+data[i]+"</option>";
            $('#plan_types').html(content);
            $('#plan_types').selectpicker('refresh');

            get_body();
        });
}

// called for only real template
function get_body() {
    // $('.page-loader').show();

    get_filters();
    // get_filters_label();
    $.post(
        '/_benchmarking',
        {
            industry: industries,
            head_counts: head_counts,
            others: others,
            regions: regions,
            plan_type: plan_type,
            states: states,
            // industry_label: industries_label,
            // head_counts_label: head_counts_label,
            // others_label: others_label,
            // regions_label: regions_label,

            bnchmrk_benefit: bnchmrk_benefit,
            // plan: plan
        },
        function(data) {
            $('.benefit-content').html(data);
            update_properties();

            update_content(bnchmrk_benefit, plan_type);
        });

    $.post(
        '/get_plans',
        {
            benefit: bnchmrk_benefit,
            plan_type: plan_type
        },
        function(data) {
            $('#plans').html(data);
            $('#plans').selectpicker('refresh');
        })        
}

update_content = function(benefit, plan_type) {
    // $('.btn-print-report').hide();
    // $('.btn-print-page').show();

	if ($.inArray(benefit, ["STRATEGY"]) != -1) {
        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, true);
        
        draw_bar_chart(benefit+'-1', gh1_data, 'dollar', 6.8);        
        draw_bar_chart(benefit+'-2', gh2_data, 'dollar', 6.8);        
    } else if ($.inArray(benefit, ["LIFE"]) != -1) {
        if (plan_type != "Flat Amount")
            $('.flat-benefit').remove();
        else
            $('.multiple-benefit').remove();        

        gh1_data = generate_quintile_data(gh1_data);
        gh2_data = generate_quintile_data(gh2_data);
        
        draw_bar_chart(benefit+'-1', gh1_data, 'dollar', 6.7);                
        draw_bar_chart(benefit+'-2', gh2_data, 'dollar', 6.7);        

        draw_donut_chart('donut-chart', gh3_data);
        draw_hbar_chart('bar-chart', gh4_data, 'percent');
      
        draw_easy_pie_chart();
    } else if ($.inArray(benefit, ["STD", "LTD"]) != -1) {
        gh1_data = generate_quintile_data(gh1_data);

        if ( benefit == "LTD")
            gh2_data = generate_quintile_data(gh2_data, true);
        else
            gh2_data = generate_quintile_data(gh2_data);
        
        draw_bar_chart(benefit+'-1', gh1_data, 'dollar', 7);        
        draw_bar_chart(benefit+'-2', gh2_data, 'int', 7.2);        

        draw_donut_chart('donut-chart', gh3_data);
        draw_hbar_chart('bar-chart', gh4_data, 'percent');
      
        // draw_easy_pie_chart();
    } else if ($.inArray(benefit, ["VISION"]) != -1) {
        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, true);
        gh3_data = generate_quintile_data(gh3_data);
        gh4_data = generate_quintile_data(gh4_data);
        gh5_data = generate_quintile_data(gh5_data, true);
        gh6_data = generate_quintile_data(gh6_data, true);        
        
        draw_bar_chart(benefit+'-1', gh1_data, 'dollar', 7);        
        draw_bar_chart(benefit+'-2', gh2_data, 'dollar', 7);        
        draw_bar_chart(benefit+'-3', gh3_data, 'dollar', 7);        
        draw_bar_chart(benefit+'-4', gh4_data, 'dollar', 7);        
        draw_bar_chart(benefit+'-5', gh5_data, 'dollar', 7);        
        draw_bar_chart(benefit+'-6', gh6_data, 'dollar', 7);        

        draw_donut_chart('donut-chart', gh7_data);
    } else if ($.inArray(benefit, ["DENTAL"]) != -1) {
        if (plan_type == "DMO")
            $('.out-benefit').remove();

        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data);
        gh3_data = generate_quintile_data(gh3_data, true);
        gh4_data = generate_quintile_data(gh4_data);
        gh6_data = generate_quintile_data(gh6_data, true);
        gh7_data = generate_quintile_data(gh7_data, true);
        gh8_data = generate_quintile_data(gh8_data, true);
        gh9_data = generate_quintile_data(gh9_data, true);
        gh10_data = generate_quintile_data(gh10_data, true);        
        
        draw_bar_chart('DENTAL-1', gh1_data, 'dollar', 7);        
        draw_bar_chart('DENTAL-2', gh2_data, 'dollar', 7);        
        draw_bar_chart('DENTAL-3', gh3_data, 'dollar', 7);        
        draw_bar_chart('DENTAL-4', gh4_data, 'dollar', 7);        
        draw_bar_chart('DENTAL-6', gh6_data, 'percent', 7);       
        draw_bar_chart('DENTAL-7', gh7_data, 'percent', 7);        
        draw_bar_chart('DENTAL-8', gh8_data, 'percent', 7);        
        draw_bar_chart('DENTAL-9', gh9_data, 'dollar', 6.8);        
        draw_bar_chart('DENTAL-10', gh10_data, 'dollar', 6.8);        

        draw_donut_chart('donut-chart', gh11_data);
        draw_hbar_chart('bar-chart', gh12_data, 'percent');

    } else if ($.inArray(benefit, ["MEDICALRX"]) != -1) {
        if (plan_type == "HMO")
            $('.out-benefit').remove();
        else if (plan_type == 'HDHP')
            $('.hdhp-benefit').remove();
        else
            $('.ppo-benefit').remove();

        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, true);
        gh3_data = generate_quintile_data(gh3_data, true);
        gh4_data = generate_quintile_data(gh4_data, true);
        gh5_data = generate_quintile_data(gh5_data, true);
        gh6_data = generate_quintile_data(gh6_data, true);
        gh8_data = generate_quintile_data(gh8_data, true);
        gh9_data = generate_quintile_data(gh9_data, true);
        
        draw_bar_chart('MEDICAL-1', gh1_data, 'dollar', 6.8);        
        draw_bar_chart('MEDICAL-2', gh2_data, 'dollar', 6.8);        
        draw_bar_chart('MEDICAL-3', gh3_data, 'dollar', 6.8);        
        draw_bar_chart('MEDICAL-4', gh4_data, 'dollar', 6.8);                
        draw_bar_chart('MEDICAL-5', gh5_data, 'dollar', 7);        
        draw_bar_chart('MEDICAL-6', gh6_data, 'dollar', 7);        
        draw_bar_chart('MEDICAL-8', gh8_data, 'dollar', 7);        
        draw_bar_chart('MEDICAL-9', gh9_data, 'dollar', 7);        

        draw_donut_chart('donut-chart', gh10_data);
        draw_hbar_chart('bar-chart', gh11_data, 'percent');
        draw_easy_pie_chart();
    }

    $('.page-loader').fadeOut();
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

function update_properties() {
	var print_template = false;

    if (!print_template) 
        if (plan != -2) // not changed benefit
            plan = $('#plans').val();
        else
            plan = 0;
    else
        plan = -1;

    if (plan == null)
    	return;
    
    $.post(
        '/update_properties',
        {
            benefit: bnchmrk_benefit,
            plan_type: plan_type,
            plan: plan
        },
        function(data) {
            if (plan == 0)
                $('.toggle_plan').hide();
            else
                $('.toggle_plan').show();
            
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