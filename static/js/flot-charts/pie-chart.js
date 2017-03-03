function draw_donut_chart() {    
    if ($('.easy-pie')[0]) {
        easyPieChart('easy-pie', '#eee', '#ccc', '#2196F3', 4, 'butt', 95);
    }

    // if ($('.L-3')[0]) {
    //     easyPieChart('L-3', '#eee', '#ccc', '#FFC107', 4, 'butt', 95);
    // }
}


/*
 * Easy Pie Charts - Used in widgets
 */
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