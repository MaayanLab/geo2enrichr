
var BaseScraper = function(notifier) {

	var scrapedData = {};

	return {

		getData: function($modal) {
			var result;
			if ($modal) {
				this.getOptions($modal);
			}
			if (this.isValidData(scrapedData)) {
				result = $.extend({}, scrapedData);
				// TODO!!!!
				//ui.fill_confirm_tbl(result);
				return result;
			}
		},

		setData: function(key, val) {
			// Store any data we might overwrite.
			var temp = scrapedData[key];
			if (key == 'cell' || key == 'platform') {
				val = val.replace(/_|-|\./g, '');
			}
			scrapedData[key] = val;
			if (this.isValidData(scrapedData)) {
				// TODO: This should be handled by UI!
				ui.fill_confirm_tbl($.extend({}, scrapedData));	
			} else {
				scrapedData[key] = temp;
			}
		},

		scrapeData: function($modal) {
			var samples = this.getSamples();

			// `__scrape_options()` and `__scrape_annotations()` are called on `getData()`,
			// i.e. when the user clicks submit.
			scrapedData.control      = samples.control;
			scrapedData.experimental = samples.experimental;
			scrapedData.accession    = this.getAccession();
			scrapedData.organism     = this.getOrganism();
			scrapedData.platform     = this.getPlatform();

			if (this.isValidData(scrapedData)) {
				return $.extend({}, scrapedData);
			}
			return undefined;
		},

		getOptions: function($modal) {
			var method = $modal.find('input[type=radio][name=method]:checked').val(),
				inclusion = $modal.find('input[type=radio][name=inclusion]:checked').val(),
				cell = $modal.find('#g2e-confirm-cell').text(),
				perturbation = $modal.find('#g2e-confirm-pert').text();

			if (method) {
				scrapedData.method = method;
			}
			if (inclusion) {
				scrapedData.inclusion = inclusion;	
			}

			if (cell) {
				scrapedData.cell = cell.replace(/_|\.|-/, '');
			}
			if (perturbation) {
				scrapedData.perturbation = perturbation.replace(/_|\.|-/, '');	
			}
		},

		textFromHtml: function($el) {
			if (!($el instanceof $)) {
				$el = $($el);
			}

			return $el.contents().filter(function() {
				return this.nodeType == 3;
			}).text().trim();
		},

		normalizeText: function(el) {
			return el.replace(/\s/g, '').toLowerCase();
		},

		isValidData: function(data) {
			/*if (!data.control || data.control.length < 2) {
				notifier.warn('Please select 2 or more control samples');
				return false;
			}
			if (!data.experimental || data.experimental.length < 2) {
				notifier.warn('Please select 2 or more experimental samples');
				return false;
			}*/
			return true;
		}
	};	
};
