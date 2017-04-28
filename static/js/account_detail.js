$(document).ready(function(){
    get_body();

    $('#profile-main li').each(function() {
        if (benefit == $(this).find('a').html()) {
            $(this).addClass('active');
        }
    });

    $('#profile-main li').click(function() {
        $('#profile-main li').removeClass('active');
        $(this).addClass('active');

        benefit = $('#profile-main li.active a').html();
        get_body();            
    });
});

function get_body() {
    $.post('/account_detail_benefit',
        {
            benefit: benefit,
            employer_id: employer_id
        },
        function(data) {
            $('#card_body').html(data);
            if ($('.selectpicker').length > 0) {
                $('.selectpicker').selectpicker();
            }
        });     
}

function toggle_edit(obj) {
    $(obj).closest("div.row").find('div.fg-line').removeClass('disabled');
    $(obj).closest("div.row").find('div.fg-line').addClass('fg-toggled');    
    $(obj).closest("div.row").find('input').removeAttr('disabled');
    $(obj).closest("div.row").find('select.selectpicker').removeAttr('disabled');
    if ($(obj).closest("div.row").find('select.selectpicker').length > 0) {
        $(obj).closest("div.row").find('select.selectpicker').selectpicker('refresh');
    }

    $(obj).closest("div.row").find('div.action').removeClass('hidden');
}

function cancel_edit(obj) {
    $(obj).closest("div.row").find('div.fg-line').addClass('disabled');
    $(obj).closest("div.row").find('div.fg-line').removeClass('fg-toggled');    
    $(obj).closest("div.row").find('input').attr('disabled', true);
    $(obj).closest("div.row").find('select.selectpicker').attr('disabled', true);
    if ($(obj).closest("div.row").find('select.selectpicker').length > 0) {
        $(obj).closest("div.row").find('select.selectpicker').selectpicker('refresh');
    }

    $(obj).closest("div.row").find('div.action').addClass('hidden');
}

function save_benefit(e, form, id) {
    $.post($(form).attr('action'),
        $(form).serialize(),
        function(data) {
            $('#'+id).html(data);
            if ($('.selectpicker').length > 0) {
                $('.selectpicker').selectpicker();
            }
        });     
 
    e.preventDefault();
}