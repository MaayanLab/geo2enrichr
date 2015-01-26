
var Comm = function(events, notifier, targetApp, SERVER) {

	// We need to make back-to-back AJAX requests to get the relevant data.
	// The steps:
	// 1. Query GEO's esearch endpoint with an accession number returns some
	//    JSON with an ID.
	// 2. Query GEO's esummary endpoint with the ID.
	// 3. Fire an event so that any modules that want this data can subscribe.
	//
	// This is *not* an IIFE because the scraper must first collect the accession
	// from the URL.
	var fetchMetadata = function(accession) {
		var EUTILS_BASE = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
			DB = 'db=gds',
			SETTINGS = '&retmax=1&retmode=json',
			EUTILS_SEARCH = EUTILS_BASE + 'esearch.fcgi?' + DB + SETTINGS,
			EUTILS_SUMMARY = EUTILS_BASE + 'esummary.fcgi?' + DB + SETTINGS;
		$.ajax({
			url: EUTILS_SEARCH + '&term=' + accession + '[ACCN]',
			type: 'GET',
			success: function(search_data) {
				var id = search_data.esearchresult.idlist[0];
				$.ajax({
					url: EUTILS_SUMMARY + '&id=' + id,
					type: 'GET',
					success: function(summaryData) {
						events.fire('metadataFetched', summaryData.result[id]);
					},
					error: errorHandler
				});
			}
		});
	};
	
	var fetchGeneList = function() {
		$.ajax({
			url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('geneListFetched', data);
			}
		});
	}();

	var fetchRareDiseases = function() {
 		$.ajax({
			url: SERVER + 'diseases?foo=bar',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('rareDiseasesFetched', data.rare_diseases);
			}
		});       
	}();

	var getAjax = function(endpoint, data, callback) {
        return $.ajax({
            url: SERVER + endpoint,
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            crossDomain: true,
            success: callback
        });
	};

	// This is the workhorse function that chains together multiple AJX requests to the back-end.
	var downloadDiffExp = function(input, app) {
		function dlgeo() {
			var data = {
                accession: input.accession,
                organism: input.organism,
                platform: input.platform,
                method: input.method,
                cell: input.cell,
                perturbation: input.perturbation,
                gene: input.gene,
                disease: input.disease
            };
			
			var success = function(data) {
                if (isError(data)) {
                    errorHandler(data);
                    return;
                }
                notifier.log('GEO files were downloaded');
                notifier.log(data);
                events.fire('progressBar');
            };

			return getAjax('dlgeo', data, success);
		}

		function diffexp(dlgeoData) {
			var data = {
                // This is the SOFT file, not the gene file.
                accession: input.accession,
                filename: dlgeoData.filename,
                platform: input.platform,
                organism: input.organism,
                control: input.control.join('-'),
                experimental: input.experimental.join('-'),
                cell: input.cell,
                perturbation: input.perturbation,
                gene: input.gene,
                disease: input.disease,
                method: input.method
            };

			var success = function(data) {
                if (isError(data)) {
                    errorHandler(data);
                    return;
                }
                var DIR = 'static/genes/';
                notifier.log('GEO files were differentially expressed');
                notifier.log(data);
                events.fire('progressBar');
                events.fire('dataDiffExped', {
                    'up': SERVER + DIR + data.up,
                    'down': SERVER + DIR + data.down
                });
            };

			return getAjax('diffexp', data, success);
		}
		
		function pipe(diffExpData) {
		    debugger;
            var data = {
                'targetApp': app,
                'up': diffExpData.up,
                'down': diffExpData.down,
                'combined': diffExpData.combined
            };

            var success = function(data) {
                if (isError(data)) {
                    errorHandler(data);
                    return;
                }
                notifier.log('Enrichr link was returned');
                notifier.log(data);
                events.fire('progressBar');
                events.fire('genesEnriched', data);
            };

            return getAjax('pipe', data, success);
        }

		// Pass in noops so that we do nothing if the promise is not returned.
		dlgeo().then(diffexp, $.noop).then(pipe, $.noop);
	};

    var isError = function(data) {
        return data.status === 'error';
    };

	var errorHandler = function(data) {
		events.fire('requestFailed', data);
	};

	return {
		downloadDiffExp: downloadDiffExp,
		fetchMetadata: fetchMetadata
	};
};
