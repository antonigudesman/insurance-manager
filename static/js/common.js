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
