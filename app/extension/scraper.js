var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.scraper = {};

	var __scraped_data = {};

	app.scraper.get_data = function() {
		return __scraped_data;
	};

	app.scraper.set_data = function(key, val) {
		__scraped_data[key] = val;
		
		app.ui.fill_confirm_tbl(
			app.scraper.__validate_data(
				$.extend({}, __scraped_data)
			)
		);
	};

	app.scraper.scrape_data = function($modal) {
		var samples = app.scraper.get_samples();

		__scraped_data.control			= samples.control;
		__scraped_data.experimental		= samples.experimental;
		__scraped_data.accession_num	= app.scraper.get_accession_num();
		__scraped_data.species			= app.scraper.get_species();
		__scraped_data.platform			= app.scraper.get_platform();
		__scraped_data.options			= app.scraper.__get_options($modal);

		return app.scraper.__validate_data( $.extend({}, __scraped_data) );
	};

	app.scraper.__validate_data = function(scraped_data) {
		if (!scraped_data.control || scraped_data.control.length < 2) {
			scraped_data.control = '<span class="g2e-highlight">Select >2 control samples</span>';
		} else {
			scraped_data.control = '<span class="g2e-strong">' + scraped_data.control.join(', ') + '</span>';
		}

		if (!scraped_data.experimental || scraped_data.experimental.length < 2) {
			scraped_data.experimental = '<span class="g2e-highlight">Select >2 experimental samples</span>';
		} else {
			scraped_data.experimental = '<span class="g2e-strong">' + scraped_data.experimental.join(', ') + '</span>';
		}

		scraped_data.accession_num = '<span class="g2e-strong">' + scraped_data.accession_num + '</span>';
		scraped_data.species 	   = '<span class="g2e-strong">' + scraped_data.species 	  + '</span>';
		scraped_data.platform 	   = '<span class="g2e-strong">' + scraped_data.platform 	  + '</span>';

		return scraped_data;
	};

	app.scraper.__get_options = function($modal) {
		return {
			method: $modal.find('input[type=radio][name=method]:checked').val(),
			inclusion: $modal.find('input[type=radio][name=inclusion]:checked').val()
		};
	};

	app.scraper.text_from_html = function($el) {
		if (!($el instanceof $)) {
			$el = $($el);
		}

		return $el.contents().filter(function() {
			return this.nodeType == 3;
		}).text().trim();
	};

	app.scraper.clean_text = function(el) {
		return el.replace(/\s/g, '').toLowerCase();
	};

})(GEO2Enrichr, jQuery);