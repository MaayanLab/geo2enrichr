
var BaseScraper = function(DEBUG, events) {

	var scrapedData = {};

	var genemap;

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

			return $.extend({}, scrapedData);
		},

		setData: function(key, val) {
			if (key == 'cell' || key == 'platform') {
				val = val.replace(/_|-|\./g, '');
			}
			scrapedData[key] = val;
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
		}
	};	
};
