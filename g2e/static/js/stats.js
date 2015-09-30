function buildStats(stats) {
    console.log(stats);

    var categories = [],
        series = [],
        key,
        value;

    series[0] = {
        data: [],
        realData: [],
        showInLegend: false,
        name: 'Gene signature'
    };
    for (key in stats.platform_counts) {
        categories.push(key);
        value = stats.platform_counts[key];
        series[0].data.push(Math.log(value) / Math.LN10);
    }

    $('#platforms-bar-chart').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Gene signatures by platform'
        },
        subtitle: {
            text: 'Log10 Scale'
        },
        xAxis: {
            categories: categories,
            //crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of gene signatures'
            }
        },
        tooltip: {
            formatter: function() {
                return '' +
                    '<p style="margin:0;">' + this.x + '</p>' +
                    '<p style="margin:0;">' + Math.round(Math.pow(10, this.y)) + '</p>';
            },
            useHTML: true
        },
        series: series
    });
}