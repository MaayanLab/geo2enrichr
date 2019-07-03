
/* Communicates to external resources, such as G2E and Enrichr's APIs.
 */
var Comm = function(events, LoadingScreen, notifier, SERVER) {

    var loadingScreen = LoadingScreen('Processing data. This may take a minute.');

    /* An IIFE that fetches a list of genes from Enrichr for autocomplete.
     */
    (function fetchGeneList() {
        post_through_background({
            query: 'Enrichr/json/genemap.json',
        })
            .then(function (data) { console.log(data); events.fire('geneListFetched', data); })
            .catch(function (error) { console.error(error); });
    })();

    /* POSTs user data to G2E servers.
     */
    function postSoftFile(inputData) {
        loadingScreen.start();
        var ONE_SECOND = 1000,
            start = time();
        post_through_background({
            query: 'api/extract/geo',
            body: inputData,
        })
            .then(function (data) {
                var id = data.extraction_id,
                    url = SERVER + 'results/' + id;
                events.fire('resultsReady', url);
            })
            .catch(handleError)
            .finally(function () { loadingScreen.stop(); });
    }

    function time() {
        return new Date().getTime();
    }

    function checkIfProcessed(payload, callback) {
        loadingScreen.start();
        post_through_background({
            query: 'crowdsourcing/check_geo',
            body: payload,
        })
            .then(function (response) { callback(response === 'exist'); })
            .catch(function (err) { notifier.warn('Unknown error.'); })
            .finally(function () { loadingScreen.stop(); });
    }

    function checkIfDuplicate(payload, callback) {
        loadingScreen.start();
        post_through_background({
            query: 'api/check_duplicate',
            body: payload,
        })
            .then(function (data) {
                if (data.preexisting) {
                    var links = data.links.join('\n');
                    alert('Match(es) found:\n\n' + links);
                } else {
                    alert('No match found.');
                }
            })
            .catch(handleError)
            .finally(function () { loadingScreen.stop(); });
    }

    // Why did I make this function? I have no idea.
    function get(url, cb) {
        $.get(url, cb);
    }

    /* Utility function for displaying error message to user.
     */
    function handleError(data) {
        var errorMsg = JSON.parse(data.responseText).error;
        events.fire('resultsError', errorMsg);
        alert(errorMsg);
    }

    return {
        checkIfProcessed: checkIfProcessed,
        checkIfDuplicate: checkIfDuplicate,
        postSoftFile: postSoftFile,
        get: get
    };
};
