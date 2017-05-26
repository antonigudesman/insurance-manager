function up(e, obj) {
	var elem = $(obj).closest('.col-md-offset-1');
	elem.insertBefore(elem.prev());
	e.preventDefault();
	return false;
}

function down(e, obj) {
	var elem = $(obj).closest('.col-md-offset-1');
	elem.insertAfter(elem.next());
	return false;
}