function buildStats(stats) {

    var categories = [],
        series = [],
        value,
        platform_counts = stats.platform_counts;

    series[0] = {
        data: [],
        realData: [],
        showInLegend: false,
        name: 'Gene signature'
    };

    platform_counts.sort(function(a, b) {
        if (a.count > b.count)
            return -1;
        if (a.count < b.count)
            return 1;
        return 0;
    });

    $.each(platform_counts, function(i, obj) {
        categories.push(obj.platform);
        series[0].data.push(Math.log(obj.count) / Math.LN10);
    });

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
            categories: categories
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Gene signatures'
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