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