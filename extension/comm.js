var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.comm = {};

	var ENDPOINT = 'g2e/',
		SERVER = 'http://localhost:8083/' + ENDPOINT,
		$dl_iframe = $('<iframe>', { id: 'g2e-dl-iframe' }).hide().appendTo('body'),
		file_for_download;

	// This pre-fetches some data from GEO to verify the information on the page!
	app.comm.fetch_meta_data_from_geo = function(acc_num) {
		var EUTILS_BASE = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
			DB = 'db=gds'
			SETTINGS = '&retmax=1&retmode=json',
			EUTILS_SEARCH = EUTILS_BASE + 'esearch.fcgi?' + DB + SETTINGS,
			EUTILS_SUMMARY = EUTILS_BASE + 'esummary.fcgi?' + DB + SETTINGS;
		$.ajax({
			url: EUTILS_SEARCH + '&term=' + acc_num + '[ACCN]',
			type: 'GET',
			success: function(search_data) {
				var id = search_data.esearchresult.idlist[0];
				$.ajax({
					url: EUTILS_SUMMARY + '&id=' + id,
					type: 'GET',
					success: function(summary_data) {
						app.global = $.extend({}, app.global, summary_data.result[id]);
					}
				});
			}
		});
	};

	app.comm.dl_url = function(url) {
		$dl_iframe.attr('src', url);
	};

	// We need to make back-to-back AJAX requests to get the relevant data.
	// Querying GEO's esearch endpoint with an accession number returns some JSON with an ID.
	// Then we query GEO's esummary endpoint with the ID.
	// Finally, we set the returned data in `app.globals` so that we can use it later.
	app.comm.fetch_diffexp_enrich = function($modal) {
		var user_input = app.scraper.get_data($modal);
		app.ui.show_progress_bar();
		app.ui.highlight_next_step();

		function dlgeo() {
			var endpoint = 'dlgeo?',
				qs = $.param({
					accession: user_input.accession_num,
					organism: user_input.organism,
					platform: user_input.platform,
					method: user_input.method,
					cell: user_input.cell,
					perturbation: user_input.perturbation
				});

			return $.ajax({
				url: SERVER + endpoint + qs,
				type: 'GET',
				success: function(data) {
					app.notifier.log('GEO files were downloaded');
					app.notifier.log(data);
					app.ui.highlight_next_step();
				}
			});
		}

		function diffexp(data_from_dlgeo) {
			var endpoint = 'diffexp?',
				qs = $.param({
					// This is the SOFT file, not the gene file.
					filename: data_from_dlgeo.filename,
					platform: user_input.platform,
					method: user_input.method,
					control: user_input.control.join('-'),
					experimental: user_input.experimental.join('-')
				});

			return $.ajax({
				url: SERVER + endpoint + qs,
				type: 'GET',
				success: function(data) {
					app.notifier.log('GEO files were differentially expressed');
					app.notifier.log(data);

					// Pass inclusion data to `download_diff_exp_files()` and `submit_data_to_enrich()`.
					data.inclusion = user_input.inclusion;
					app.ui.highlight_next_step();
				}
			});
		}

		function enrichr(data_from_diffexp) {
			var endpoint = 'enrichr?',
				filename = data_from_diffexp[data_from_diffexp.inclusion],
				qs = 'filename=' + filename;

			file_for_download = filename;
			$.ajax({
				url: SERVER + endpoint + qs,
				type: 'GET',
				success: function(data) {
					app.notifier.log('Enrichr link was returned');
					app.notifier.log(data);
					app.ui.highlight_next_step();
					app.ui.show_results(data.link);
				}
			});
		}

		dlgeo().then(diffexp).then(enrichr);
	};

	app.comm.download_diff_exp_files = function() {
		app.notifier.log('Downloading files locally');
		app.notifier.log(file_for_download);
		app.comm.dl_url(SERVER + file_for_download);
	};

	app.comm.reset_downloaded_file = function() {
		file_for_download = undefined;
	};

})(GEO2Enrichr, jQuery);