
var Comm = function(events, notifier, SERVER) {

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
        console.log("POSTING");
        var $loader = $('<div class="g2e-loader-container"><div class="g2e-loader-modal">Processing data. This may take a minute.</div></div>');
        $('body').append($loader);
        $.post(SERVER + 'api/extract/geo',
            input,
            function(data) {
                if (!!data.error) {
                    events.fire('resultsError');
                } else {
                    var id = data.extraction_id,
                        url = SERVER + '#results/' + id;
                    events.fire('resultsReady', url);
                }
            })
            .fail(function(xhr, status, error) {
                console.log("FAILED:");
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
