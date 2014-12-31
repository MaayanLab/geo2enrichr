
var BaseScraper = function(DEBUG, events, notifier) {

	var scrapedData = {};

	var genemap;

	events.on('genemapDownloaded', function(data) {
		genemap = data;
	});

	return {

		getData: function($modal) {
			// getSamples() returns an object rather than mutating scrapedData
			// because the function must be mixed in at runtime.
			var samples = this.getSamples();
			if ($modal) {
				this.getOptions($modal);
			}

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

		setData: function(key, val) {
			// Store any data we might overwrite.
			var temp = scrapedData[key];
			if (key == 'cell' || key == 'platform') {
				val = val.replace(/_|-|\./g, '');
			}
			scrapedData[key] = val;
			if (!this.isValidData(scrapedData)) {
				// Reset if necessary.
				scrapedData[key] = temp;
			}
		},

		getOptions: function($modal) {
			var method = $modal.find('input[type=radio][name=method]:checked').val(),
				cell = $modal.find('#g2e-confirm-cell td').eq(1).text(),
				perturbation = $modal.find('#g2e-confirm-pert td').eq(1).text(),
				gene = $modal.find('#g2e-confirm-gene #genemap').val();

			if (method) {
				scrapedData.method = method;
			}
			if (cell) {
				scrapedData.cell = cell.replace(/_|\.|-/, '');
			}
			if (perturbation) {
				scrapedData.perturbation = perturbation.replace(/_|\.|-/, '');	
			}
			if (gene) {
				scrapedData.gene = gene;
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
			if (!DEBUG) {
				if (!data.control || data.control.length < 2) {
					notifier.warn('Please select 2 or more control samples');
					return false;
				}
				if (!data.experimental || data.experimental.length < 2) {
					notifier.warn('Please select 2 or more experimental samples');
					return false;
				}
				// It is important to verify that the user has *tried* to select a gene before warning them
				// because this code executes every time the data is validated.
				if (genemap && data.gene && !$.inArray(data.gene, genemap)) {
					notifier.warn('Please input a valid gene.');
					return false;
				}
				return true;
			} else {
				return true;
			}
		}
	};	
};
