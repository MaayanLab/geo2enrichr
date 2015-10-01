$(function() {

    var loader = Loader(),
        FADE_IN_SPEED = 600,
        FADE_OUT_SPEED = 600,
        vizTool2Func,
        RESULTS_PAGE_BASE = 'http://amp.pharm.mssm.edu/g2e/results/';

    vizTool2Func = {
        'clustergrammer': function() {
            var promises = buildPromises();
            $.when.apply($, promises).done(requestClustergrammer);
        },
        'pca': function() {
            var extractionIds = getExtractionIds();
            requestPca(extractionIds);
        }
    };

    $('#consensus .options button').click(visualizeGeneSignatures);

    function visualizeGeneSignatures() {
        var app = $('#consensus select').find(":selected").attr('data-app');
        if (typeof vizTool2Func[app] === 'function') {
            loader.start();
            vizTool2Func[app]();
        } else {
            alert('No visualization tool selected.');
        }
    }

    /* Clustergrammer
     * -------------- */
    function buildPromises() {
        var $inputs = $('input.consensus'),
            promises = [];
        $inputs.each(function(i, checkbox) {
            var $checkbox = $(checkbox);
            if ($checkbox.is(':checked')) {
                promises.push(getAjax($checkbox.attr('name')));
            }
        });
        return promises;
    }

    function getAjax(extractionId) {
        return $.ajax({
            url: 'api/extract/' + extractionId,
            method: 'GET'
        });
    }

    function getCombinedList(geneLists) {
        for (var i = 0; i < geneLists.length; i++) {
            if (geneLists[i].direction === 0) {
                return geneLists[i].ranked_genes;
            }
        }
        return [];
    }

    function requestClustergrammer() {
        var geneSignatures = [];
        $.each(arguments, function(i, response) {
            var signature = response[0];
            geneSignatures.push({
                col_title: signature.extraction_id,
                link: RESULTS_PAGE_BASE + signature.extraction_id,
                genes: getCombinedList(signature.gene_lists)
            });
        });

        $.ajax({
            url: 'http://amp.pharm.mssm.edu/clustergrammer/g2e/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                description: 'TODO',
                link: window.location.href,
                gene_signatures: geneSignatures
            }),
            success: embedIframe,
            complete: function() {
                loader.stop();
            }
        });
    }

    function embedIframe(data) {
        var $cg = $('#clustergrammer-preview');
        $cg.fadeIn(FADE_IN_SPEED);
        $cg.find('iframe').attr('src', data.preview_link);
        $cg.find('a').attr('href', data.link);
        $cg.find('button').click(function() {
            $cg.fadeOut(FADE_OUT_SPEED);
        });
    }


    /* Principal Component Analysis
     * ---------------------------- */
    function requestPca(extractionIds) {
        $.ajax({
            url: 'pca',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(extractionIds),
            success: displayPca,
            complete: function() {
                loader.stop();
            }
        });
    }

    function displayPca(data) {
        var $container = $('#pca-container');
        function tooltipFormatter() {
            return '<a href="results/' + this.key + '" target="_blank">' + this.key + '</a>';
        }
        $container.fadeIn(FADE_IN_SPEED);
        plotPCA(JSON.parse(data), 'pca-visualization', tooltipFormatter);
        $container.find('button').click(function() {
            $container.fadeOut(FADE_OUT_SPEED);
        });
    }

    function getExtractionIds() {
        var $inputs = $('input.consensus'),
            extractionIds = [];
        $inputs.each(function(i, checkbox) {
            var $checkbox = $(checkbox);
            if ($checkbox.is(':checked')) {
                extractionIds.push($checkbox.attr('name'));
            }
        });
        return extractionIds;
    }
});