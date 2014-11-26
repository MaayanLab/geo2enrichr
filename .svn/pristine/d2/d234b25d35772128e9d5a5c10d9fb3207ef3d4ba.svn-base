var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.comm = {};

	var SERVER = 'http://localhost:5000/';

	var $dl_iframe = $('<iframe>', { id: 'g2e-dl-iframe' }).hide().appendTo('body');

	// This pre-fetches some data from GEO to verify the information on the page!
	app.comm.fetch_meta_data_from_geo = function(acc_num) {
		var EUTILS_BASE = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
			DB = 'db=gds'
			SETTINGS = '&retmax=1&retmode=json',
			EUTILS_SEARCH = EUTILS_BASE + 'esearch.fcgi?' + DB + SETTINGS,
			EUTILS_SUMMARY = EUTILS_BASE + 'esummary.fcgi?' + DB + SETTINGS,

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
	app.comm.fetch_files_from_geo = function($modal) {
		var user_input = app.scraper.get_data($modal);

		function dlgeo() {
			var endpoint = 'dlgeo?',
				qs = $.param({
					accession: user_input.accession_num,
					species: user_input.species,
					platform: user_input.platform,
					method: user_input.options.method
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
					filename: data_from_dlgeo.filename,
					method: user_input.options.method,
					control: user_input.control.join('-'),
					experimental: user_input.experimental.join('-')
				});

			return $.ajax({
				url: SERVER + endpoint + qs,
				type: 'GET',
				success: function(data) {
					app.notifier.log('GEO files were differentially expressed');
					app.notifier.log(data);

					// Pass inclusion data to `download_diff_exp_files()`.
					data.inclusion = user_input.options.inclusion;
					app.ui.highlight_next_step();
				}
			});
		}

		// Return a promise so that client functions can continue chaining.
		return dlgeo().then(diffexp);
	};

	app.comm.download_diff_exp_files = function() {

		app.ui.show_progress_bar();

		app.comm.fetch_files_from_geo().then(function(data_from_diffexp) {
			var base_url = SERVER + data_from_diffexp.directory,
				inclusion = data_from_diffexp.inclusion;

			app.ui.highlight_next_step();
			app.notifier.log('Downloading files locally');
			app.notifier.log(data_from_diffexp);

			if (inclusion === 'up' || inclusion === 'down') {
				app.comm.dl_url(base_url + data_from_diffexp[inclusion]);
			} else {
				app.comm.dl_url(base_url + data_from_diffexp.up);
				// Chrome doesn't have time to download the first file without a delay.
				setTimeout(function() {
					app.comm.dl_url(base_url + data_from_diffexp.down);
				}, 1000);
			}
		});
	};

	app.comm.submit_data_to_enrich = function($modal) {

		app.ui.show_progress_bar();

		app.comm.fetch_files_from_geo().then(function(data_from_diffexp) {
			var endpoint = 'enrichr?',
				qs = 'files=';

			qs += data_from_diffexp.up   ? data_from_diffexp.up   : '';
			qs += '-';
			qs += data_from_diffexp.down ? data_from_diffexp.down : '';

			$.ajax({
				url: SERVER + endpoint + qs,
				type: 'GET',
				success: function(data) {
					app.notifier.log('Enrichr links were returned');
					app.notifier.log(data);
					app.ui.highlight_next_step();
					app.ui.handle_enrichr_links(data.links);
				}
			});
		});
	};

})(GEO2Enrichr, jQuery);