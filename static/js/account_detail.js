var benefit = 'EMPLOYER';

$(document).ready(function(){
    get_body();

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
        });     
}

function toggle_edit(obj) {
    $(obj).closest("div.row").find('div.fg-line').removeClass('disabled');
    $(obj).closest("div.row").find('div.fg-line').addClass('fg-toggled');    
    $(obj).closest("div.row").find('input').removeAttr('disabled');

    $(obj).closest("div.row").find('div.action').removeClass('hidden');
}

function cancel_edit(obj) {
    $(obj).closest("div.row").find('div.fg-line').addClass('disabled');
    $(obj).closest("div.row").find('div.fg-line').removeClass('fg-toggled');    
    $(obj).closest("div.row").find('input').attr('disabled', true);

    $(obj).closest("div.row").find('div.action').addClass('hidden');
}