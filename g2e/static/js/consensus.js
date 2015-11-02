$(function() {

    var loader = Loader(),
        FADE_IN_SPEED = 600,
        FADE_OUT_SPEED = 600,
        vizTool2Func,
        RESULTS_PAGE_BASE = 'http://amp.pharm.mssm.edu/g2e/results/';

    vizTool2Func = {
        'clustergrammer': function() {
            var chbxs = getSelectedCheckboxes(),
                promises;
            if (isValidSelection(chbxs)) {
                loader.start();
                promises = buildPromises(chbxs);
                $.when.apply($, promises).done(requestClustergrammer);
            }
        },
        'pca': function() {
            var chbxs = getSelectedCheckboxes(),
                extractionIds;
            if (isValidSelection(chbxs, 'pca')) {
                loader.start();
                extractionIds = getExtractionIds(chbxs);
                requestPca(extractionIds);
            }
        }
    };

    var $dataTables = $('.data-table');
    $dataTables.dataTable({
        bPaginate: true,
        fnInitComplete: function() {
            $dataTables.fadeIn();
        }
    });

    $('#consensus .options button').click(visualizeGeneSignatures);

    function visualizeGeneSignatures() {
        var app = $('#consensus select').find(":selected").attr('data-app');
        if (typeof vizTool2Func[app] === 'function') {
            vizTool2Func[app]();
        } else {
            alert('No visualization tool selected.');
        }
    }

    /* Clustergrammer
     * -------------- */
    function buildPromises(chbxs) {
        var promises = [];
        $.each(chbxs, function(i, checkbox) {
            promises.push(getAjax(checkbox.extractionId));
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
        plotPCA(data, 'pca-visualization', tooltipFormatter);
        $container.find('button').click(function() {
            $container.fadeOut(FADE_OUT_SPEED);
        });
    }

    function getExtractionIds(chbxs) {
        var extractionIds = [];
        $.each(chbxs, function(i, checkbox) {
            extractionIds.push(checkbox.extractionId);
        });
        return extractionIds;
    }

    /* Helper function for collecting data from selected checkboxes.
     */
    function getSelectedCheckboxes() {
        var selected = [];
        $('input.consensus').each(function(i, checkbox) {
            var $checkbox = $(checkbox);
            if ($checkbox.is(':checked')) {
                selected.push({
                    extractionId: $checkbox.attr('name'),
                    platform: $checkbox.closest('tr').find('.platform').text()
                });
            }
        });
        return selected;
    }

    /* Helper function that validates the selected checkboxes, alerting and
     * returning false if invalid.
     */
    function isValidSelection(chbxs, vizType) {
        var isValid,
            platform;
        if (chbxs.length === 0) {
            alert('Heyo, no selection.');
            return false;
        }
        if (vizType === 'pca' && chbxs.length < 3) {
            alert('3D PCA requires at least 3 dimensions.');
            return false;
        }

        isValid = true;
        platform = chbxs[0].platform;
        $.each(chbxs, function(i, obj) {
            if (obj.platform !== platform) {
                isValid = false;
                return false; // Early return.
            }
        });

        if (!isValid) {
            alert('Every gene signature must come from the same platform.');
        }

        return isValid;
    }
});