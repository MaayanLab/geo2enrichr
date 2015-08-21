
/* Communicates to external resources, such as G2E and Enrichr's APIs.
 */
var Comm = function(events, loader, notifier, SERVER) {

    /* An IIFE that fetches a list of genes from Enrichr for autocomplete.
     */
    var fetchGeneList = (function() {
        try {
            $.ajax({
                url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
                type: 'GET',
                dataType: 'JSON',
                success: function(data) {
                    events.fire('geneListFetched', data);
                }
            });
        } catch (err) {
        }
    })();

    /* POSTs user data to G2E servers.
     */
    var postSoftFile = function(input) {
        loader.start();
        $.post(SERVER + 'api/extract/geo',
            input,
            function(data) {
                if (!!data.error) {
                    events.fire('resultsError');
                } else {
                    var id = data.extraction_id,
                        url = SERVER + 'results/' + id;
                    events.fire('resultsReady', url);
                }
            })
            .fail(function(xhr, status, error) {
                events.fire('resultsError');
            })
            .always(function() {
                loader.stop();
            });
    };

    return {
        postSoftFile: postSoftFile
    };
};
