var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.scraper = {};

	var __scraped_data = {};

	app.scraper.get_data = function($modal) {
		var scraped_data;
		if ($modal) {
			app.scraper.__scrape_options_and_annotations($modal);
		}
		if (app.scraper.is_valid_data(__scraped_data)) {
			scraped_data = $.extend({}, __scraped_data);
			app.ui.fill_confirm_tbl(scraped_data);	
			return scraped_data;
		}
	};

	app.scraper.set_data = function(key, val) {
		// Store any data we might overwrite.
		var temp = __scraped_data[key];
		if (key == 'cell' || key == 'platform') {
			val = val.replace(/_|-|\./g, '')
		}
		__scraped_data[key] = val;
		if (app.scraper.is_valid_data(__scraped_data)) {
			app.ui.fill_confirm_tbl($.extend({}, __scraped_data));	
		} else {
			__scraped_data[key] = temp;
		}
	};

	app.scraper.scrape_data = function($modal) {
		var samples = app.scraper.get_samples();

		// `__scrape_options()` and `__scrape_annotations()` are called on `get_data()`,
		// i.e. when the user clicks submit.
		__scraped_data.control       = samples.control;
		__scraped_data.experimental  = samples.experimental;
		__scraped_data.accession_num = app.scraper.get_accession_num();
		__scraped_data.organism      = app.scraper.get_organism();
		__scraped_data.platform      = app.scraper.get_platform();

		if (app.scraper.is_valid_data(__scraped_data)) {
			return $.extend({}, __scraped_data);
		}
	};

	app.scraper.__scrape_options_and_annotations = function($modal) {
		var method = $modal.find('input[type=radio][name=method]:checked').val(),
			inclusion = $modal.find('input[type=radio][name=inclusion]:checked').val(),
			cell = $modal.find('#g2e-confirm-cell').text(),
			perturbation = $modal.find('#g2e-confirm-pert').text();

		if (method) {
			__scraped_data.method = method;
		}
		if (inclusion) {
			__scraped_data.inclusion = inclusion;	
		}

		if (cell) {
			__scraped_data.cell = cell.replace(/_|\.|-/, '');
		}
		if (perturbation) {
			__scraped_data.perturbation = perturbation.replace(/_|\.|-/, '');	
		}
	};

	app.scraper.text_from_html = function($el) {
		if (!($el instanceof $)) {
			$el = $($el);
		}

		return $el.contents().filter(function() {
			return this.nodeType == 3;
		}).text().trim();
	};

	app.scraper.normalize_text = function(el) {
		return el.replace(/\s/g, '').toLowerCase();
	};

	app.scraper.is_valid_data = function(data) {
		// This is annoying while testing.
		if (!app.debug) {
			if (!data.control || data.control.length < 2) {
				app.notifier.warn('Please select 2 or more control samples');
				return false;
			}
			if (!data.experimental || data.experimental.length < 2) {
				app.notifier.warn('Please select 2 or more experimental samples');
				return false;
			}
		}
		return true;
	};

})(GEO2Enrichr, jQuery);