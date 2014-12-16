var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.gse = {};

	app.gse.key = 'gse';

	var $overlay,
		$modal,
		$hook,
		$gse_details,
		$samples_table;

	app.gse.init = function() {
		// Setup the correct scraper.
		app.scraper = $.extend({}, app.scraper, app.gse._scraper);

		// Go up two parents to find the table.
		$hook = $('#geo2r').next();

		// Find the details table.
		$('table').each(function(i, el) {
			var $el = $(el);
			if ($el.attr('width') === '600' &&
				$el.attr('cellpadding') === '2' &&
				$el.attr('cellspacing') === '0')
			{
				$gse_details = $el;
				return false;
			}
		});

		// Find the samples from the details table.
		$gse_details.find('tr').each(function(i, tr) {
			if ($(tr).find('td')
					 .first()
					 .text()
					 .toLowerCase()
					 .indexOf('samples') === 0)
			{
				$samples_table = $(tr);
				return false;
			}
		});

		// This executes in the background, collecting information about the page before the user even inputs.
		app.global.accession = app.scraper.__get_acc_from_url();
		app.comm.fetch_meta_data_from_geo(app.global.accession);

		app.gse.embed();
	};

	app.gse.embed = function() {
		$hook.append(app.html.get('btn'));
		$('#g2e-link').click(function() {
			app.ui.on_open_app($hook);
		});

		$samples_table.find('tr').each(function(i, tr) {
			$(tr).append(app.html.get('chkbxs'));
		});

		$samples_table.find('table')
					  .first()
					  .find('tr')
					  .first()
					  .before(app.html.get('thead'));
	};

	// This will be mixed in with the base scraper.
	app.gse._scraper = {

		// The accession number is not necessarily in the URL for GDS.
		// Should we check anyway?
		get_accession_num: function() {
			return app.global.accession;
		},

		get_organism: function() {
			return app.global.taxon || app.scraper.__get_by_name('organism');
		},

		get_platform: function() {
			return app.scraper.__get_by_name('platforms');
		},

		get_samples: function() {
			var control = [],
				experimental = [];

			$('.g2e-chkbx').each(function(i, input) {
				var $input = $(input),
					gene;
				if ($input.is(':checked')) {
					gene = $(input).parent()
								   .siblings()
								   .first()
								   .find('a')
								   .text();

					if ($input.hasClass('g2e-control')) {
						control.push(gene);
					} else if ($input.hasClass('g2e-experimental')) {
						experimental.push(gene);
					}
				}
			});

			return {
				control: control,
				experimental: experimental
			};
		},

		__get_by_name: function(name) {
			var idx = app.scraper.__get_row_idx_from_name(name);
			return $($gse_details.find('tr')[idx]).find('a').text();
		},

		__get_row_idx_from_name: function(attr_name) {
			var result;
			$gse_details.find('tr').each(function(i, tr) {
				var text = $(tr).find('td')
								.first()
								.text();
				text = app.scraper.normalize_text(text).replace(/[^a-zA-Z]/g, '');

				if (text === attr_name) {
					result = i;
					return false;
				}
			});
			return result;
		},

		// If required, this can be used as a general purpose query param getter.
		__get_acc_from_url: function() {
			var field_name = 'acc',
				params = window.location.search.substring(1).split('&'),
				i = 0,
				len = params.length;

			for (; i < len; i++)  {
				var key_val = params[i].split('=');
				if (key_val[0] == field_name) {
					return key_val[1];
				}
			}
		}
	};

})(GEO2Enrichr, jQuery);