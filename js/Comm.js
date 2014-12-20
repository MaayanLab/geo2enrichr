
var Comm = function(events, notifier, scraper, SERVER) {

	var ENTRY_POINT = 'g2e/',
		fileForDownload = [];

	// We need to make back-to-back AJAX requests to get the relevant data.
	// Querying GEO's esearch endpoint with an accession number returns some JSON with an ID.
	// Then we query GEO's esummary endpoint with the ID.
	// Finally, we fire an event so that any modules that want this data can subscribe.
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
					}
				});
			}
		});
	};

	// This is the workhorse function that chains together multiple AJX requests to the back-end.
	var downloadDiffexpEnrich = function($modal) {
		var userInput = scraper.getData($modal);

		function dlgeo() {
			var endpoint = 'dlgeo?',
				qs = $.param({
					accession: userInput.accession,
					organism: userInput.organism,
					platform: userInput.platform,
					method: userInput.method,
					cell: userInput.cell,
					perturbation: userInput.perturbation
				});

			return $.ajax({
				url: SERVER + ENTRY_POINT + endpoint + qs,
				type: 'GET',
				success: function(data) {
					notifier.log('GEO files were downloaded');
					notifier.log(data);
					events.fire('progressBar');
				}
			});
		}

		function diffexp(dlgeoData) {
			var endpoint = 'diffexp?',
				qs = $.param({
					// This is the SOFT file, not the gene file.
					filename: dlgeoData.filename,
					platform: userInput.platform,
					method: userInput.method,
					inclusion: userInput.inclusion,
					control: userInput.control.join('-'),
					experimental: userInput.experimental.join('-')
				});

			return $.ajax({
				url: SERVER + ENTRY_POINT + endpoint + qs,
				type: 'GET',
				success: function(data) {
					notifier.log('GEO files were differentially expressed');
					notifier.log(data);
					events.fire('progressBar');
				}
			});
		}

		function enrichr(diffexpData) {
			var endpoint = 'enrichr?',
				qs;

			fileForDownload = diffexpData.filename;
			qs = 'filename=' + fileForDownload;

			$.ajax({
				url: SERVER + ENTRY_POINT + endpoint + qs,
				type: 'GET',
				success: function(data) {
					notifier.log('Enrichr link was returned');
					notifier.log(data);
					events.fire('progressBar');
					data.fileForDownload = SERVER + 'static/genes/' + fileForDownload;
					events.fire('dataDownloaded', data);
				}
			});
		}

		dlgeo().then(diffexp).then(enrichr);
	};

	return {
		downloadDiffexpEnrich: downloadDiffexpEnrich,
		fetchMetadata: fetchMetadata
	};
};
