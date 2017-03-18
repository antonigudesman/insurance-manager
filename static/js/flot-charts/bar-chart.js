function NormalDensityZx(x, Mean, StdDev)
{
    var a = x - Mean;
    return Math.exp(-(a * a) / (2 * StdDev * StdDev)) / (Math.sqrt(2 * Math.PI) * StdDev); 
}

function draw_bar_chart(id, data, tip=true, xticks=0) {       
    // var ticks = [["0%", "0%"], ["20%", "20%"], ["40%", 20], ["60%", 30], ["80%", 40]];
    var ticks = ["0%", "20%", "40%", "60%", "80%", "100%"];
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
                autoscaleMargin: -0.1
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
                mode: 'categories',
                min: 0,
                tickSize: 20,
                // ticks: ticks
            },
    
            legend:{
                container: '.flc-bar',
                backgroundOpacity: 0.5,
                noColumns: 0,
                backgroundColor: "white",
                lineWidth: 0
            },

        });

        if (tip) {
            $.each(p.getData()[0].data, function(i, el){
                var o = p.pointOffset({x: i, y: el[1]});
                if (el[1] != 0.0) {
                    $('<div class="data-point-label">' + el[1] + '%</div>').css( {
                        position: 'absolute',
                        left: o.left - 24,
                        top: o.top - 20,
                        display: 'none'
                    }).appendTo(p.getPlaceholder()).fadeIn('slow');                
                }
            });                    
        }

        // if (xticks) {
        //     var ticks_ = p.getAxes().xaxis.ticks;
        //     for (var i = 0; i < ticks_.length; i++) {
        //         p.getAxes().xaxis.ticks[i]['v'] += " %";
        //         p.getAxes().xaxis.ticks[i]['label'] += " %";
        //     }

        //     console.log(p.getAxes().xaxis.ticks);
        //     p.setupGrid();
        //     p.draw();
        // }
    }    
}