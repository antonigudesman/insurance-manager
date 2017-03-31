function digits(digit_str) {
    return digit_str.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
}

var yaxis_formatter = [];

yaxis_formatter['dollar'] = function(val, axis) {
    return '$' + digits(val.toString());
}

yaxis_formatter['percent'] = function(val, axis) {
    return digits(val.toString()) + '%';
}

yaxis_formatter['int'] = function(val, axis) {
    return digits(val.toString());
}

function draw_bar_chart(id, data, unit, label_xpos_factor) {       
    // This is not a bar chart anymore.
    // This is a incremental stack chart with color coding
    tickFormatter = yaxis_formatter[unit];
    
    if (typeof label_xpos_factor === 'undefined')
        label_xpos_factor = 6.5;

    var ticks = [[0, "0%"], [20, "20%"], [40, "40%"], [60, "60%"], [80, "80%"]];

    if ($('#'+id)[0]) {
        var p = $.plot($('#'+id), data, {
            grid : {
                borderWidth: 1,
                show : true,
                hoverable : true,
                clickable : true,
                borderColor: '#ddd',
            },
            
            yaxis: {
                tickColor: '#eee',
                tickDecimals: 0,
                tickFormatter: tickFormatter,
                font :{
                    lineHeight: 15,
                    style: "normal",
                    color: "#b3b3b3",
                    size: 14
                },
                shadowSize: 0,
                autoscaleMargin: -0.1,
                // min: 0,
                // ticks: [],
            },
            
            xaxis: {
                tickColor: '#eee',
                tickDecimals: 0,
                font :{
                    lineHeight: 13,
                    style: "normal",
                    color: "rgb(94, 94, 94)",
                    size: 14
                },
                shadowSize: 0,
                // mode: 'categories',
                min: 0,
                tickSize: 20,
                ticks: ticks
            },
    
            legend:{
                container: '.flc-bar',
                backgroundOpacity: 0.5,
                noColumns: 0,
                backgroundColor: "white",
                lineWidth: 0
            },
        });

        var UNIT = {
            'dollar': '$',
            'percent': '%',
            'int': ''
        };

        $.each(p.getData()[0].data, function(i, el){
            var o = p.pointOffset({x: i, y: el[1]});
            var content = UNIT[unit] + digits(el[1].toString());
            if (unit == 'percent')
                content = digits(el[1].toString()) + UNIT[unit];

            if (el[0] % 20 == 0) {
                $('<div class="data-point-label"><b>' + content + '</b></div>').css( {
                    position: 'absolute',
                    left: 30 + el[0] * label_xpos_factor,
                    top: o.top - 25,
                    display: 'none'
                }).appendTo(p.getPlaceholder()).fadeIn('slow');                
            }
        });                    
    }    
}