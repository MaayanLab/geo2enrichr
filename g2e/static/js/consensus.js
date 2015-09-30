$(function() {

    $('button').click(visualizeGeneSignatures);

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

    function visualizeGeneSignatures() {
        var promises = buildPromises();
        $.when.apply($, promises).done(requestClustergrammer);
    }

    function buildPromises() {
        var $inputs = $('input'),
            promises = [];
        $inputs.each(function(i, checkbox) {
            var $checkbox = $(checkbox);
            if ($checkbox.is(':checked')) {
                promises.push(getAjax($checkbox.attr('name')));
            }
        });
        return promises;
    }

    function requestClustergrammer() {
        var CLUSTERGRAMMER_URL = 'http://amp.pharm.mssm.edu/clustergrammer/g2e/',
            geneSignatures = [];

        $.each(arguments, function(i, response) {
            var signature = response[0];
            geneSignatures.push({
                name: signature.extraction_id,
                genes: getCombinedList(signature.gene_lists)
            });
        });

        $.ajax({
            url: CLUSTERGRAMMER_URL,
            method: 'POST',
            data: JSON.stringify({
                gene_signatures: geneSignatures
            }),
            success: function() {
                debugger;
            }
        });
    }
});