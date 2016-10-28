
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
        var ONE_SECOND = 1000,
            start = time();
        $.post(SERVER + 'api/extract/geo',
            inputData,
            function(data) {
                if (!!data.error) {
                    handleError(data);
                } else {
                    var id = data.extraction_id,
                        url = SERVER + 'results/' + id;
                    events.fire('resultsReady', url);
                }
            })
            .fail(function(data) {
                handleError(data);
            })
            .always(function() {
                loadingScreen.stop();
            });
    }

    function time() {
        return new Date().getTime();
    }

    function checkIfProcessed(payload, callback) {
        loadingScreen.start();
        $.post(
            'http://maayanlab.net/crowdsourcing/check_geo.php',
            payload,
            function(response) {
                callback(response === 'exist');
            })
            .error(function(data) {
                notifier.warn('Unknown error.');
            })
            .always(function() {
                loadingScreen.stop();
            });
    }

    function checkIfDuplicate(payload, callback) {
        loadingScreen.start();
        $.ajax({
            url: SERVER + 'api/check_duplicate',
            type: 'GET',
            data: payload,
            success: function(data) {
                if (data.preexisting) {
                    var links = data.links.join('\n');
                    alert('Match(es) found:\n\n' + links);
                } else {
                    alert('No match found.');
                }
            },
            error: handleError,
            complete: function() {
                loadingScreen.stop();
            }
        });
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
