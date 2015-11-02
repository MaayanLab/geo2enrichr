function buildStats(stats) {

    Highcharts.setOptions({
        colors: ['#005f99'],
        chart: {
            style: {
                fontFamily: 'Open Sans'
            }
        }
    });

    var categories = [],
        series = [],
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
        if (obj.count > 1) {
            series[0].data.push(Math.log(obj.count) / Math.log(10));
            categories.push(obj.platform);
        }
    });

    $('#platforms-bar-chart').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: ''
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
            useHTML: true,
            crosshairs: true
        },
        series: series
    });
}