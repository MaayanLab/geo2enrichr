
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
        $.post(SERVER + 'extract',
            input,
            function(data) {
                var id = data.extraction_id,
                    url = SERVER + '#results/' + id;
                events.fire('resultsReady', url);
            }
        );
    };

    return {
        postSoftFile: postSoftFile
    };
};
