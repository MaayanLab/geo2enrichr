var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.gds = {};

	app.gds.key = 'gds';

	var $overlay,
		$modal,
		$hook,
		$gds_details;

	app.gds.init = function() {
		// Setup the correct scraper.
		app.scraper = $.extend({}, app.scraper, app.gds._scraper);

		var id = setInterval(function() {
			$hook = $('#diff_express > tbody');
			if ($hook.length) {

				$gds_details = $('#gds_details');

				// This executes in the background, collecting information about the page before the user even inputs.
				app.global.accession = app.scraper.__get_acc_from_page();
				app.comm.fetch_meta_data_from_geo(app.global.accession);

				app.gds.embed();

				clearInterval(id);
			}
		}, 250);
	};

	app.gds.embed = function() {
		var html = app.html.get('btn');
		$hook.children().last().after(html);
		$('#g2e-link').click(function() {
			app.ui.on_open_app($hook);
		});
	};

	// This will be mixed in with the base scraper.
	app.gds._scraper = {

		get_accession_num: function() {
			return app.global.accession || app.gds.__get_acc_from_page();
		},

		get_organism: function() {
			return app.scraper.__get_by_name('organism');
		},

		get_platform: function() {
			return app.scraper.__get_by_name('platform');
		},

		get_samples: function() {
			var $groupRow = $($hook.children().find('tbody td')[0]),
				bkp_not_found = true,
				samplesStr = app.scraper.text_from_html($groupRow),
				samplesArr = samplesStr.split(' '),
				samples_bkp_idx, control, experimental;

			$.each(samplesArr, function(i, val) {
				if (bkp_not_found && val.substr(val.length-1) !== ',') {
					samples_bkp_idx = i+1;
					bkp_not_found = false;
				} else {
					// WARNING: we're mutating the list while iterating over it. 
					// This should be okay since we're just trimming the comma.
					samplesArr[i] = val.replace(',', '');
				}
			});

			return {
				control: samplesArr.slice(0, samples_bkp_idx),
				experimental: samplesArr.slice(samples_bkp_idx, samplesArr.length)
			};
		},

		__get_by_name: function(name) {
			// 1. Grab the text from the appropriate row
			// 2. Strip out all the whitespace (newlines, tabs, etc.)
			// 3. Split on the semicolon (notice there are two) and return just the code.
			var idx = app.scraper.__get_row_idx_from_name(name);
			var text = $($gds_details.find('tr')[idx]).text();
			// Regular expression removes any preceding whitespace
			return text.split(':')[1].replace(/\s*/, '');
		},

		__get_row_idx_from_name: function(attr_name) {
			var result;
			$gds_details.find('tr').each(function(i, tr) {
				var title_el = $(tr).find('th')[0],
					title_text = app.scraper.normalize_text($(title_el).text()),
					title_name = title_text.split(':')[0];

				if (title_name === attr_name) {
					result = i;
					return false;
				}
			});
			return result;
		},

		__get_acc_from_page: function() {
			var record_caption = $gds_details.find('.caption').text(),
				re = new RegExp(/(?:GDS|GSE)[0-9]*/);
			return re.exec(record_caption)[0];
		}
	};

})(GEO2Enrichr, jQuery);