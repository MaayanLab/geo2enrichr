
var Comm = function(events, notifier, targetApps, SERVER) {

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
			url: SERVER + 'diseases',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('rareDiseasesFetched', data.rare_diseases);
			}
		});       
	}();

	// This is the workhorse function that chains together multiple AJX requests to the back-end.
	var downloadDiffExp = function(input) {
  
        var getPost = function(endpoint, data, callback) {
            return $.ajax({
                url: SERVER + endpoint,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json;charset=UTF-8',
                crossDomain: true,
                success: callback
            });
        };

        var isError = function(data) {
            return data.status === 'error';
        };

        var errorHandler = function(data) {
            events.fire('requestFailed', data);
        };

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

			return getPost('dlgeo', data, success);
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

			return getPost('diffexp', data, success);
		}

		function pipe(diffExpData) {
            var data = {
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

            return getPost(targetApps.current().endpoint, data, success);
        }

		// Pass in noops so that we do nothing if the promise is not returned.
		dlgeo().then(diffexp, $.noop).then(pipe, $.noop);
	};

	return {
		downloadDiffExp: downloadDiffExp
	};
};
