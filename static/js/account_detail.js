$(document).ready(function(){
    var grid = $(".data-table-benefit").bootgrid({
        caseSensitive: false,
        css: {
            icon: 'zmdi icon',
            iconColumns: 'zmdi-view-module',
            iconDown: 'zmdi-expand-more',
            iconRefresh: 'zmdi-refresh',
            iconUp: 'zmdi-expand-less'
        },
        templates: {
            footer: "",
            header: ''
        },        
        formatters: {
            "link": function(column, row) {
                return "<a href='javascript:void(0);' class='link-edit' data-row-id='"+row.id+"' data-row-benefit='"+row.benefit+"' data-row-title='"+row.title+"'>"+row[column.id]+"</a>";
            }
        }
    }).on("loaded.rs.jquery.bootgrid", function() {
        /* Executes after data is loaded and rendered */
        grid.find(".link-edit").on("click", function(e)
        {
            var benefit = $(this).data("row-benefit");
            var plan_name = $(this).data("row-title");

            $.post('/account_detail_benefit',
                {
                    benefit: $(this).data("row-benefit"),
                    plan: $(this).data("row-id")
                },
                function(data) {
                    $('#card_body').html(data);
                    if ($('.selectpicker').length > 0) {
                        $('.selectpicker').selectpicker();
                    }
                });     

            // manipulate breadcrumb
            var employer_name = $('ol.breadcrumb li.active').html().replace('&amp;', '&');
            var benefit_dict = {
                'MEDICAL': 'Medical & Rx',
                'DENTAL': 'Dental',
                'VISION': 'Vision',
                'LIFE': 'Life',
                'STD': 'STD',
                'LTD': 'LTD',
                'STRATEGY': 'Strategy'
            }
            
            if (employer_name != benefit_dict[benefit]+' - '+plan_name) {
                console.log(employer_name);
                console.log(benefit_dict[benefit]+' - '+plan_name);
                $('ol.breadcrumb li.active').remove();
                $('ol.breadcrumb').append('<li><a href="javascript:location.reload();">'+employer_name+'</a></li>');
                $('ol.breadcrumb').append('<li class="active">'+benefit_dict[benefit]+' - '+plan_name+'</li>');                
            }
        });
    });
});

function toggle_edit(obj) {
    $('div.fg-line').removeClass('disabled');
    $('div.fg-line').addClass('fg-toggled');    
    $('input').removeAttr('disabled');
    $('select.selectpicker').removeAttr('disabled');
    if ($('select.selectpicker').length > 0) {
        $('select.selectpicker').selectpicker('refresh');
    }

    $('div.action').removeClass('hidden');
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
            $('#'+id).html(data['body']);
            if (!data['is_valid']) {
                toggle_edit($('#action-edit'));
            }

            if ($('.selectpicker').length > 0) {
                $('.selectpicker').selectpicker();
            }
        });     
 
    e.preventDefault();
}