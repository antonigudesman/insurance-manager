function up(e, obj) {
	var elem = $(obj).closest('.col-md-offset-1');
	elem.insertBefore(elem.prev());
}

function down(e, obj) {
	var elem = $(obj).closest('.col-md-offset-1');
	elem.insertAfter(elem.next());
}

function get_order() {
	var print_order = [];
	// window.status = 'Printing...';
	swal('Printing report...');
	
	$('.panel').each(function() {
		var model = {};
		var attrs = [], attrs_inv = [], attrs_srv = [];

		model.benefit = $(this).data('benefit');
		model.plan = $(this).data('plan');
		model.title = $(this).data('title');
		model.plan_type = $(this).data('plan_type');

		$(this).find('select.property_inv').each(function(){
			attrs_inv.push($(this).val());
		});

		$(this).find('select.property').each(function(){
			attrs.push($(this).val());
		});

		$(this).find('select.service').each(function(){
			attrs_srv.push($(this).val());
		});

		model.quintile_properties = attrs;
		model.quintile_properties_inv = attrs_inv;
		model.services = attrs_srv;
		print_order.push(model);
	});

    $.post(
        '/print_report_in_order',
        { print_order: JSON.stringify(print_order) },
        function(filename) {
        	// window.status = '';
            window.location = '/download_report/'+filename;
        });
}