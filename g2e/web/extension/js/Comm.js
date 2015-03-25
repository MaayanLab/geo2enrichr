
var Comm = function(events, notifier, targetApps, SERVER) {

    var fetchGeneList = (function() {
        $.ajax({
            url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
            type: 'GET',
            dataType: 'JSON',
            success: function(data) {
                events.fire('geneListFetched', data);
            }
        });
    })();

    var postSoftFile = function(input) {
        var $loader = $('<div class="g2e-loader-container"><div class="g2e-loader-modal">Loading...</div></div>');
        $('body').append($loader);
        $.post(SERVER + 'api/extract/geo',
            input,
            function(data) {
                var id = data.extraction_id,
                    url = SERVER + '#results/' + id;
                events.fire('resultsReady', url);
            })
            .fail(function() {
                events.fire('resultsError');
            })
            .always(function() {
                $loader.remove();
            });
    };

    return {
        postSoftFile: postSoftFile
    };
};
