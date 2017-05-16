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

    var ticks = [[0, "0%"], [10, "10%"], [20, "20%"], [30, "30%"], [40, "40%"], [50, "50%"], [60, "60%"], [70, "70%"], [80, "80%"], [90, "90%"], [100, "100%"],];

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
    }    
}

function draw_hbar_chart(id, barData, unit) {
    if ($('#'+id)[0]) {
        var p = $.plot($("#"+id), barData, {
            grid : {
                    borderWidth: 1,
                    borderColor: '#eee',
                    show : true,
                    hoverable : true,
                    clickable : true
            },
            
            yaxis: {
                tickColor: '#eee',
                tickDecimals: 0,
                font :{
                    lineHeight: 13,
                    style: "normal",
                    color: "#9f9f9f",
                },
                shadowSize: 0,
                tickFormatter: yaxis_formatter[unit]
            },
            
            xaxis: {
                tickColor: '#fff',
                tickDecimals: 0,
                font :{
                    lineHeight: 13,
                    style: "normal",
                    color: "#9f9f9f"
                },
                shadowSize: 0,
                mode: 'categories'
            },
    
            legend:{
                container: '.flc-bar',
                backgroundOpacity: 0.5,
                noColumns: 0,
                backgroundColor: "white",
                lineWidth: 0
            }
        });         
    }

}