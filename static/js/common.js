if ($('#industries').length > 0) {
    $('#industries').change(function() {
        refresh_content();
    });

    $('#regions').change(function() {
        refresh_content();
    });

    $('#head-counts').change(function() {
        refresh_content();
    });

    $('#other_filter').change(function() {
        refresh_content();
    });    

    if ($('#plan_types').length > 0) {
        $('#plan_types').change(function() {
            reload_plans();
            refresh_content();
        });                    
    }

    if ($('#states').length > 0) {
        $('#states').change(function() {
            refresh_content();
        });                    
    }
}

function get_filters() {
    industries = [];
    regions = [];
    head_counts = [];
    others = [];
    states = [];

    if ($('#plan_types').length > 0) {
        plan_type = $('#plan_types').val();
    }

    if ($('#states').length > 0) {
        $('#states :selected').each(function() {
            states.push($(this).val());
        });
    }

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
    states_label = [];

    if ($('#states').length > 0) {
        $('#states :selected').each(function() {
            states.push($(this).html());
        });
    }

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

    if (states_label.length == 0)
        states_label.push('All');
}
