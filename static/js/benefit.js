var industries = [];
var regions = [];
var head_counts = [];
var others = [];
var states = [];

var plan = 0;
var quintile_properties = [];
var quintile_properties_inv = [];
var services = [];

var industry_label = [];
var head_counts_label = [];
var others_label = [];
var regions_label = [];
var states_label = [];
var colors;

if (broker == 'namely') {
    colors = ['#D9575A', '#D9575A', '#FF9496', '#FF9496', '#CDC9C2', '#CDC9C2', '#36A9D9', '#36A9D9', '#0061BB', '#0061BB'];
} else {
    colors = ['#f8696b', '#f8696b', '#FFE364', '#FFE364', '#bfbfbf', '#bfbfbf', '#B1D480', '#B1D480', '#63be7b', '#63be7b'];
}

jQuery(function($) {
    if (print_template == true) {
        update_properties();
        update_content(bnchmrk_benefit, plan_type);
    } else if (print_template == false) {    
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
    }
});

function update_quintile(obj, graph_holder, qscore_holder, inverse) {
    property = $(obj).val();
    type = $(obj).find(':selected').attr('type');

    // change the id of q-score placeholder
    $('.'+qscore_holder).attr('id', 'prop_rank_'+property);
    get_dynamic_attributes();

    $.post(
        '/update_quintile',
        {
            plan: plan,
            property: property,
            type: type,
            inverse: inverse,

            quintile_properties: quintile_properties,
            quintile_properties_inv: quintile_properties_inv,
            services: services            
        },
        function(data) {
            if (!plan || plan == "0")
                $('.toggle_plan').hide();
            else
                $('.toggle_plan').show();

            for (i=0; i < attribute_map.length; i++) {
                if (typeof attribute_map[i][data['property']] != 'undefined' ) {
                    attribute_map[i].data = data['graph'];
                    break;
                }
            }

            gh_data = generate_quintile_data(data['graph'], inverse);        

            var value = data['qscore'];
            if (value != 'N/A') {
                $('.'+qscore_holder).html(value);
                $('.'+qscore_holder).removeAttr('style');
                $('.'+qscore_holder).css('color', colors[parseInt(value/10)]);

                var ya = data['val'];
                if (ya < data['graph'][0][1])
                    ya = data['graph'][0][1];

                if (ya > data['graph'][10][1])
                    ya = data['graph'][10][1];

                // draw cirlces
                gh_data.push(
                    {
                        data: [[value, ya]],
                        points: { show: true, radius: 4 },
                        lines: { show: false, fill: 0.98 },
                        color: '#000000'
                    }
                );
            }
            draw_bar_chart(graph_holder, gh_data, data['type'], 6.4);        
        });
}

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

            reload_plans();   
            get_body();
        });
}

// called for only real template
function get_body() {
    get_filters();
    get_filters_label();

    $.post(
        '/_benchmarking',
        {
            industry: industries,
            head_counts: head_counts,
            others: others,
            regions: regions,
            plan_type: plan_type,
            states: states,

            industry_label: industries_label,
            head_counts_label: head_counts_label,
            others_label: others_label,
            regions_label: regions_label,
            states_label: states_label,

            bnchmrk_benefit: bnchmrk_benefit,
            // plan: plan
        },
        function(data) {
            $.post(
                '/get_num_employers',{},
                function(data) {
                    $('#num_employers').html(data);
                })

            $('.benefit-content').html(data);
            update_properties();
            $('.selectpicker').selectpicker();   

            update_content(bnchmrk_benefit, plan_type);
        });

}

function reload_plans() {
    plan_type = $('#plan_types').val();

    plan = -2;    
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
	if ($.inArray(benefit, ["STRATEGY"]) != -1) {
        draw_easy_pie_chart();
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
        gh1_data = generate_quintile_data(gh1_data, false);

        draw_bar_chart(benefit+'-1', gh1_data, 'dollar', 7);       

        draw_donut_chart('donut-chart', gh3_data);
        draw_hbar_chart('bar-chart', gh4_data, 'percent');
      
        // draw_easy_pie_chart();
    } else if ($.inArray(benefit, ["VISION"]) != -1) {
        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, false);
        gh5_data = generate_quintile_data(gh5_data, true);
        gh6_data = generate_quintile_data(gh6_data, true);        
        
        draw_bar_chart(benefit+'-1', gh1_data, 'dollar', 7);
        draw_bar_chart(benefit+'-2', gh2_data, 'dollar', 7);             
        draw_bar_chart(benefit+'-5', gh5_data, 'dollar', 7);        
        draw_bar_chart(benefit+'-6', gh6_data, 'dollar', 7);        

        draw_donut_chart('donut-chart', gh7_data);
    } else if ($.inArray(benefit, ["DENTAL"]) != -1) {
        if (plan_type == "DMO")
            $('.out-benefit').hide();

        gh1_data = generate_quintile_data(gh1_data, true);
        gh3_data = generate_quintile_data(gh3_data, false);
        gh9_data = generate_quintile_data(gh9_data, true);
        gh10_data = generate_quintile_data(gh10_data, true);        
        
        draw_bar_chart('DENTAL-1', gh1_data, 'dollar', 7);        
        draw_bar_chart('DENTAL-3', gh3_data, 'dollar', 7);           
        draw_bar_chart('DENTAL-9', gh9_data, 'dollar', 6.8);        
        draw_bar_chart('DENTAL-10', gh10_data, 'dollar', 6.8);        

        draw_donut_chart('donut-chart', gh11_data);
        draw_hbar_chart('bar-chart', gh12_data, 'percent');
        draw_easy_pie_chart();
    } else if ($.inArray(benefit, ["MEDICALRX"]) != -1) {
        if (plan_type == "HMO")
            $('.out-benefit').hide();
        else if (plan_type == 'HDHP')
            $('.hdhp-benefit').remove();
        else
            $('.ppo-benefit').remove();

        // console.log(gh1_data);
        gh1_data = generate_quintile_data(gh1_data, true);
        gh2_data = generate_quintile_data(gh2_data, true);
        gh8_data = generate_quintile_data(gh8_data, true);
        gh9_data = generate_quintile_data(gh9_data, true);
        
        // console.log(gh1_data);
        draw_bar_chart('MEDICAL-1', gh1_data, 'dollar', 6.4);        
        draw_bar_chart('MEDICAL-2', gh2_data, 'dollar', 6.8);       
        draw_bar_chart('MEDICAL-8', gh8_data, 'dollar', 7);        
        draw_bar_chart('MEDICAL-9', gh9_data, 'dollar', 7);        

        draw_donut_chart('donut-chart', gh10_data);
        draw_hbar_chart('bar-chart', gh11_data, 'percent');
        draw_easy_pie_chart();


        if ($('.stats-line')[0]) {
            sparklineLine('stats-line', [9,4,6,5,6,4,5,7,9,3,6,5], 85, 45, '#fff', 'rgba(0,0,0,0)', 1.25, 'rgba(255,255,255,0.4)', 'rgba(255,255,255,0.4)', 'rgba(255,255,255,0.4)', 3, '#fff', 'rgba(255,255,255,0.4)');
        }        
    }

    for (var i = 0; i < $('select.property').length; i++) {
        var obj = $('select.property').eq(i);
        obj.val(quintile_properties_[i]);
        obj.selectpicker('refresh');
    }

    for (var i = 0; i < $('select.property_inv').length; i++) {
        var obj = $('select.property_inv').eq(i);
        obj.val(quintile_properties_inv_[i]);
        obj.selectpicker('refresh');
    }

    for (var i = 0; i < $('select.service').length; i++) {
        var obj = $('select.service').eq(i);
        obj.val(services_[i]);
        obj.selectpicker('refresh');
    }

    $('.page-loader').fadeOut();
}

generate_quintile_data = function(raw_data, inverse){
    if (raw_data.length < 10)
        return [];

    var data = [];
    var section = [];
    var N = raw_data.length;

    for( var i = 0; i < N; i++ ) {
        var color_index = inverse ? 10 - raw_data[i][0] / 10 : raw_data[i][0] / 10 - 1;
        if (inverse)
            section.push([100-raw_data[i][0], raw_data[i][1]]);
        else
            section.push([raw_data[i][0], raw_data[i][1]]);

        if ( i >= 0 && raw_data[i][0] % 20 == 0) {
            data.push({
                data : section,
                points: { show: false },
                lines: { show: true, fill: 0.98 },
                color: colors[color_index]
            });
            if (inverse)
                section = [[100-raw_data[i][0], raw_data[i][1]]];
            else
                section = [[raw_data[i][0], raw_data[i][1]]];
        }
    }       

    return data;
}

function get_dynamic_attributes() {
    quintile_properties = [];
    $('select.property').each(function() {
        quintile_properties.push($(this).val());
    });   

    quintile_properties_inv = [];
    $('select.property_inv').each(function() {
        quintile_properties_inv.push($(this).val());
    });   

    services = [];
    $('select.service').each(function() {
        services.push($(this).val());
    });   
}

function update_properties() {
    get_dynamic_attributes();
    // get current quintile properties

    if (!print_template) {
        if (plan != -2) // not changed benefit
            plan = $('#plans').val();
        else 
            plan = 0;        
    } else {
        plan = -1;
    }

    console.log(plan);
    if (plan == null)
    	return;
    
    $.post(
        '/update_properties',
        {
            benefit: bnchmrk_benefit,
            plan: plan,
            quintile_properties: quintile_properties,
            quintile_properties_inv: quintile_properties_inv,
            services: services,
            print_template: print_template
        },
        function(data) {
            if (plan == 0 || plan == "" || data == '') {
                $('.toggle_plan').hide();
            } else {
                $('.toggle_plan').show();
                $.each(data, function( key, value ) {
                    if (key.match("^rank_")) {
                        $('#prop_'+key).html(value);
                        $('#prop_'+key).removeAttr('style');

                        if ( value != 'N/A') {
                            $('#prop_'+key).css('color', colors[parseInt(value/10)]);

                            var attr = key.substring(5);

                            if (data[attr] !== undefined && typeof attribute_map !== 'undefined') {
                                var ya = parseInt(String(data[attr]).replace(',', '').replace('$', '').replace('%', ''));
                                var gh_data, graph_holder, type, inverse;
                                // iterate attribute_map and find relevant info.
                                for (i=0; i < attribute_map.length; i++) {
                                    if (typeof attribute_map[i][attr] != 'undefined' ) {
                                        gh_data = attribute_map[i].data;
                                        graph_holder = attribute_map[i].placeholder;
                                        type = attribute_map[i][attr];
                                        inverse = attribute_map[i].inverse;                                
                                        break;
                                    }
                                }
                                
                                if (gh_data.length > 0) {
                                    if (ya < gh_data[0][1])
                                        ya = gh_data[0][1];

                                    if (ya > gh_data[10][1])
                                        ya = gh_data[10][1];
                                    // console.log(gh_data);
                                    var entry = {
                                        data: [[value, ya]],
                                        points: { show: true, radius: 4 },
                                        lines: { show: false, fill: 0.98 },
                                        color: '#000000'                                
                                    }
                                    // // get gh_data
                                    // // update it
                                    gh_data = generate_quintile_data(gh_data, inverse);
                                    gh_data.push(entry);
                                    // //redraw graph
                                    draw_bar_chart(graph_holder, gh_data, type, 6.4);        
                                }
                            } else {
                                $('select.service option').each(function() {
                                    var attr_ = $(this).val();
                                    if (key.indexOf(attr_) != -1) {
                                        $(this).closest('.e-cost-section').find('.progress-bar').css('background-color', colors[parseInt(value/10)]);                                        
                                    }
                                });
                            }
                        }
                    } else if (key.match("^service_")) {
                        var title = '';

                        if (!value) {
                            title = '-';
                        } else if (value[5] == 'FALSE') {
                            title = 'No deductible, $' + value[4] + ' copay';
                        } else if (value[5] == 'False/Coin') {
                            if (value[4]) {
                                title = '$' + value[4] + ', no deductible, coinsurance';
                            } else {
                                title = 'No deductible, then coinsurance';
                            }
                        } else if (value[5] == 'TRUE') {
                            title = 'Deductible, $' + value[4] + ' copay';
                        } else {
                            if (value[4]) {
                                title = '$' + value[4] + ', deductible, then coinsurance';
                            } else {
                                title = 'Deductible, then coinsurance';
                            }
                        }

                        $('#'+key).html(title);
                    } else {
                        $('#prop_'+key).html(value);
                    }
                });         
            }            
        });
}

function update_e_cost(obj) {
    var service = $(obj).val();
    get_dynamic_attributes();

    $.post(
        '/update_e_cost',
        {
            service: service,
            benefit: bnchmrk_benefit,
            plan_type: plan_type, 
            plan: plan,

            quintile_properties: quintile_properties,
            quintile_properties_inv: quintile_properties_inv,
            services: services
        },
        function(data) {
            var title = '';

            if (data[5] == 'FALSE')
                title = 'No deductible, $' + data[4] + ' copay ( $' + data[1] + ' )';
            else if (data[5] == 'False/Coin')
                title = 'No deductible, coinsurance (Benchmark)';
            else if (data[5] == 'TRUE')
                title = 'Deductible, $' + data[4] + ' copay (Benchmark)';
            else
                title = 'Deductible, then coinsurance (Benchmark)';

            $(obj).closest('.e-cost-section').find('.e_cost_title').html(title);
            
            var ded_percent = data[2] * 100.0 / data[1];
            var coin_percent = data[3] * 100.0 / data[1];
            var copay_percent = data[4] * 100.0 / data[1];

            $(obj).closest('.e-cost-section').find('.progress-bar-success').removeAttr('style');
            $(obj).closest('.e-cost-section').find('.progress-bar-success').css('width', ded_percent+'%');
            $(obj).closest('.e-cost-section').find('.progress-bar-warning').removeAttr('style');
            $(obj).closest('.e-cost-section').find('.progress-bar-warning').css('width', coin_percent+'%');
            $(obj).closest('.e-cost-section').find('.progress-bar-danger').removeAttr('style');
            $(obj).closest('.e-cost-section').find('.progress-bar-danger').css('width', copay_percent+'%');
            $(obj).closest('.e-cost-section').find('.percentile').attr('id', 'prop_rank_'+service);

            var value = data[6];
            if (value != 'N/A') {
                $(obj).closest('.e-cost-section').find('.percentile').html(value);
                $(obj).closest('.e-cost-section').find('.percentile').removeAttr('style');
                $(obj).closest('.e-cost-section').find('.percentile').css('color', colors[parseInt(value/10)]);
                $(obj).closest('.e-cost-section').find('.progress-bar').css('background-color', colors[parseInt(value/10)]);
            }
        });
}


function show_print_pending_dialog(id) {
    swal("Printing Page Confirmation", "Please wait while your $$$ Benchmarking Report is generated. You will be alerted as soon as the report is ready to download.".replace('$$$', bnchmrk_benefit));
    // window.open("/print_page_preview", "myWindow"+$(this).data("row-id"), "width=1400,height=600,left=200,top=200,scrollbars=yes,location=no");
}

function show_print_report_pending_dialog() {
    swal("Printing Page Confirmation", "Please wait while your Benchmarking Report is generated. You will be alerted as soon as the report is ready to download.");
}
