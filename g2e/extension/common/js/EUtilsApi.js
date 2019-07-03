
/* Wrapper for making calls to the EUtils API.
 */
function EUtilsApi(comm, events, page, screenScraper) {

    var accession = getAccession(),
        BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{0}.fcgi?db=gds&retmax=1&retmode=json';

    function init() {
        var searchUrl;
        if (!page.isGds()) {
            searchUrl = BASE_URL.replace('{0}', 'esearch') + '&term=' + accession;
            comm.get(searchUrl, function(data) {
                getDataFromGdsAccessionId(data.esearchresult.idlist[0]);
            });
        } else {
            getDataFromGdsAccessionId(accession.slice(3));
        }
    }

    function getDataFromGdsAccessionId(accessionId) {
        var summaryUrl = BASE_URL.replace('{0}', 'esummary') + '&id=' + accessionId,
            metadata = {};
        comm.get(summaryUrl, function(data) {
            data = data.result[accessionId];
            metadata.title = data.title;
            metadata.summary = data.summary;
            metadata.platform = 'GPL' + data.gpl;
            metadata.organism = data.taxon;
            events.fire('eutilsApiFetched', metadata);
        });
    }

    function getAccession() {
        return screenScraper.getDataset();
    }

    return {
        init: init
    };
}
