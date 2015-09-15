
/* Communicates to external resources, such as G2E and Enrichr's APIs.
 */
var Comm = function(events, LoadingScreen, notifier, SERVER) {

    var loadingScreen = LoadingScreen('Processing data. This may take a minute.');

    /* An IIFE that fetches a list of genes from Enrichr for autocomplete.
     */
    (function fetchGeneList() {
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
    function postSoftFile(inputData) {
        loadingScreen.start();
        $.post(SERVER + 'api/extract/geo',
            inputData,
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
                loadingScreen.stop();
            });
    }

    function checkIfProcessed(payload, callback) {
        loadingScreen.start();
        $.post(
            'http://maayanlab.net/crowdsourcing/check_geo.php',
            payload,
            function(response) {
                console.log(payload);
                callback(response === 'exist');
            })
            .error(function() {
                notifier.warn('Unknown error.');
            })
            .always(function() {
                loadingScreen.stop();
            });
    }

    function get(url, cb) {
        $.get(url, cb);
    }

    return {
        checkIfProcessed: checkIfProcessed,
        postSoftFile: postSoftFile,
        get: get
    };
};
