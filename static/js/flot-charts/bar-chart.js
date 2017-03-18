digits = function(digit_str) {
    return digit_str.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
}

function NormalDensityZx(x, Mean, StdDev)
{
    var a = x - Mean;
    return Math.exp(-(a * a) / (2 * StdDev * StdDev)) / (Math.sqrt(2 * Math.PI) * StdDev); 
}

function draw_bar_chart(id, data, tip=true, xticks=0) {       
    var ticks = [[0, "0%"], [20, "20%"], [40, "40%"], [60, "60%"], [80, "80%"]];

    if ($('#'+id)[0]) {
        var p = $.plot($('#'+id), data, {
            grid : {
                borderWidth: 1,
                show : true,
                hoverable : true,
                clickable : true,
            },
            
            yaxis: {
                tickColor: '#eee',
                tickDecimals: 0,
                font :{
                    lineHeight: 15,
                    style: "normal",
                    color: "#9f9f9f",
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
                    color: "#9f9f9f",
                    size: 12
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

        if (!tip) {
            $.each(p.getData()[0].data, function(i, el){
                var o = p.pointOffset({x: i, y: el[1]});
                if (el[0] % 20 == 0) {
                    $('<div class="data-point-label">' + '$'+digits(el[1].toString()) + '</div>').css( {
                        position: 'absolute',
                        left: 27 + el[0] * 7.5,
                        top: o.top - 25,
                        display: 'none'
                    }).appendTo(p.getPlaceholder()).fadeIn('slow');                
                }
            });                    
        }
    }    
}