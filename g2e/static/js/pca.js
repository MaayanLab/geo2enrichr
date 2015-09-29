function plotPCA (pcaObj) {

    var mins = pcaObj.ranges[1],
        maxs = pcaObj.ranges[0],
        titles = pcaObj.titles;

    var chart = new Highcharts.Chart({
        chart: {
            // zoomType:'xyz',
            renderTo: 'pca-container',
            margin: [150, 150, 150, 150],
            type: 'scatter',
            options3d: {
                enabled: true,
                alpha: 20,
                beta: 30,
                depth: 500
            }
        },
        legend: {
            floating: true,
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top'
        },
        title: {
            text: '3D PCA plot'
        },
        subtitle: {
            text: 'using x y z coordinates'
        },
        xAxis: {
            title: {text: titles[0]},
            min: mins[0],
            max: maxs[0]
        },
        yAxis: {
            title: {text: titles[1]},
            min: mins[1],
            max: maxs[1]
        },
        zAxis: {
            title: {text: titles[2]},
            min: mins[2],
            max: maxs[2]
        },
        series: pcaObj.series,
        tooltip: {
            formatter: function () {
                return this.key;
            }
        }
    });

    // Add mouse events for rotation
    $(chart.container).bind('mousedown.hc touchstart.hc', function (e) {
        e = chart.pointer.normalize(e);

        var posX = e.pageX,
            posY = e.pageY,
            alpha = chart.options.chart.options3d.alpha,
            beta = chart.options.chart.options3d.beta,
            newAlpha,
            newBeta,
            sensitivity = 5; // lower is more sensitive

        $(document).bind({
            'mousemove.hc touchdrag.hc': function (e) {
                newBeta = beta + (posX - e.pageX) / sensitivity;
                chart.options.chart.options3d.beta = newBeta;
                newAlpha = alpha + (e.pageY - posY) / sensitivity;
                chart.options.chart.options3d.alpha = newAlpha;
                chart.redraw(false);
            },
            'mouseup touchend': function () {
                $(document).unbind('.hc');
            }
        });
    });
}