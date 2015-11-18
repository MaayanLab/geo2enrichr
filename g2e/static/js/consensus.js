$(function() {

    var loader = Loader(),
        FADE_IN_OUT_SPEED = 600,
        vizToolConfig;

    vizToolConfig = {
        enrichr: {
            init: function() {
                var chbxs = getSelectedCheckboxes(),
                    promises;
                if (isValidSelection(chbxs)) {
                    loader.start();
                    requestEnrichmentResults(chbxs);
                }
            }
        },
        clustergrammer: {
            init:  function() {
                var chbxs = getSelectedCheckboxes(),
                    promises;
                if (isValidSelection(chbxs)) {
                    loader.start();
                    promises = buildPromises(chbxs);
                    $.when.apply($, promises).done(requestClustergrammer);
                }
            }
        },
        pca: {
            init: function() {
                var chbxs = getSelectedCheckboxes(),
                    extractionIds;
                if (isValidSelection(chbxs, 'pca')) {
                    loader.start();
                    extractionIds = getExtractionIds(chbxs);
                    requestPca(extractionIds);
                }
            }
        }
    };

    setupDataTables();
    setupConsensusAnalysisListener();
    setupSelectAll();

    function setupSelectAll() {
        $('#select-all').click(function(evt) {
            if ($(evt.target).prop('checked')) {
                $('input.consensus').prop('checked', true);
            } else {
                $('input.consensus').prop('checked', false);
            }
        });
    }

    function setupDataTables() {
        var $dataTables = $('.data-table');
        $dataTables.dataTable({
            bSort: false,
            bPaginate: true,
            fnInitComplete: function() {
                $dataTables.fadeIn();
            }
        });
    }

    function setupConsensusAnalysisListener() {
        var appOptions = $('.app-options');
        $('#analysis-tool').change(function(evt) {
            var app = $(evt.target).find(':selected').attr('data-app'),
                $selectedOpts = $('#consensus select[data-app-option=' + app + ']'),
                $allOpts = $('select[data-app-option]');

            $allOpts.addClass('hidden');
            $selectedOpts.removeClass('hidden');
        });
        $('#consensus .options button').click(function() {
            var app = $('#consensus select').find(":selected").attr('data-app');
            if (typeof vizToolConfig[app].init === 'function') {
                vizToolConfig[app].init();
            } else {
                alert('No visualization tool selected.');
            }
        });
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

    function requestEnrichmentResults(chbxs) {
        $.ajax({
            url: 'enrichr',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                signatures: chbxs,
                backgroundType: $('#enrichr-background').val()
            }),
            success: function(data) {
                debugger;
            }
        });
    }

    function requestClustergrammer() {
        var geneSignatures = [],
            titles = {};
        $.each(arguments, function(i, response) {
            var signature = response[0],
                sf = signature.soft_file,
                colTitle = sf.title,
                newNumTitles;

            if (sf.is_geo) {
                colTitle = sf.accession + ': ' + colTitle;
            }

            if (titles[colTitle]) {
                newNumTitles = titles[colTitle] + 1;
                titles[colTitle] = newNumTitles;
                colTitle = colTitle + newNumTitles;
            } else {
                titles[colTitle] = 1;
            }

            geneSignatures.push({
                col_title: colTitle,
                link: 'http://amp.pharm.mssm.edu/g2e/results/' + signature.extraction_id,
                genes: getCombinedList(signature.gene_lists)
            });
        });

        var data = JSON.stringify({
            description: 'TODO',
            link: window.location.href,
            gene_signatures: geneSignatures
        });
        $.ajax({
            url: 'http://amp.pharm.mssm.edu/clustergrammer/g2e/',
            method: 'POST',
            contentType: 'application/json',
            data: data,
            success: embedIframe,
            complete: function() {
                loader.stop();
            }
        });
    }

    function embedIframe(data) {
        var $cg = $('#clustergrammer-preview');
        $cg.fadeIn(FADE_IN_OUT_SPEED);
        $cg.find('iframe').attr('src', data.preview_link);
        $cg.find('a').attr('href', data.link);
        $cg.find('button').click(function() {
            $cg.fadeOut(FADE_IN_OUT_SPEED);
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
        $container.fadeIn(FADE_IN_OUT_SPEED);
        plotPCA(data, 'pca-visualization', tooltipFormatter);
        $container.find('button').click(function() {
            $container.fadeOut(FADE_IN_OUT_SPEED);
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
            alert('Please select a gene signature.');
            return false;
        }
        if (vizType === 'pca' && chbxs.length < 3) {
            alert('3D PCA requires at least 3 dimensions.');
            return false;
        }

        // Disable for now in favor of select all!
        // ---------------------------------------
        //isValid = true;
        //platform = chbxs[0].platform;
        //$.each(chbxs, function(i, obj) {
        //    if (obj.platform !== platform) {
        //        isValid = false;
        //        return false; // Early return.
        //    }
        //});
        //
        //if (!isValid) {
        //    alert('Every gene signature must come from the same platform.');
        //}

        return isValid;
    }
});