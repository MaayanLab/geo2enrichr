
/* Wrapper for making calls to the EUtils API.
 */
function EUtilsApi(comm, page, screenScraper) {

    var metadata = {},
        accession = getAccessionId();

    function getUrl() {
        var BASE_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?&retmax=1&retmode=json',
            db = page.isGds() ? 'gds' : 'geoprofiles';
        return [BASE_URL, 'db=' + db, 'id=' + accession].join('&');
    }

    function getAccessionId() {
        return screenScraper.getDataset().slice(3);
    }

    function getMetadata(callback) {
        var url = getUrl();
        comm.get(url, callback);
    }

    getMetadata(function(response) {
        metadata = response.result[accession];
    });

    return {
        getMetadata: function() {
            return metadata;
        }
    };
}
