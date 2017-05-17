function draw_easy_pie_chart() {    
    if ($('.main-pie')[0]) {
        easyPieChart('main-pie', 'rgba(255,255,255,0.2)', '#ccc', 'rgba(255,255,255,0.7)', 7, 'butt', 95);
    }

    if ($('.easy-pie-1')[0]) {
        easyPieChart('easy-pie-1', 'rgba(255,255,255,0.2)', '#ccc', '#2196f3', 7, 'butt', 95);
        // easyPieChart('main-pie', '#eee', '#ccc', 'rgba(255,255,255,0.7)', 7, 'butt', 148);
    }
}

function easyPieChart(id, trackColor, scaleColor, barColor, lineWidth, lineCap, size) {
    $('.'+id).easyPieChart({
        trackColor: trackColor,
        scaleColor: scaleColor,
        barColor: barColor,
        lineWidth: lineWidth,
        lineCap: lineCap,
        size: size
    });
}

function draw_donut_chart(id, data) {    
    if ($('#'+id)[0]) {
        $.plot($('#'+id), data, {
            series: {
                pie: {
                    innerRadius: 0.5,
                    show: true,
                    stroke: { 
                        width: 2,
                    },
                },
            },
            legend: {
                container: '.flc-donut',
                backgroundOpacity: 0.5,
                noColumns: 0,
                backgroundColor: "white",
                lineWidth: 0
            },
            // grid: {
            //     hoverable: true,
            //     clickable: true
            // },
            tooltip: true,
            tooltipOpts: {
                content: "%p.0%, %s", // show percentages, rounding to 2 decimal places
                shifts: {
                    x: 20,
                    y: 0
                },
                defaultTheme: false,
                cssClass: 'flot-tooltip'
            }
            
        });
    }
}