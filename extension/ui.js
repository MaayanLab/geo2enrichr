var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.ui = {};

	var first_click = true,

		elem_config = {
			'g2e-confirm-tbl-acc': {
				key: 'accession_num',
				prompt: 'Please enter an accession number:'
			},
			'g2e-confirm-tbl-pltf': {
				key: 'platform',
				prompt: 'Please enter a platform:'
			},
			'g2e-confirm-tbl-org' : {
				key: 'organism',
				prompt: 'Please enter an organism:'
			},
			'g2e-confirm-tbl-ctrl': {
				key: 'control',
				format: function(data) {
					return data.join(', ');
				}
			},
			'g2e-confirm-tbl-expmt': {
				key: 'experimental',
				format: function(data) {
					return data.join(', ');
				}
			},
			'g2e-confirm-cell': {
				key: 'cell',
				prompt: 'Please enter a cell type or tissue:'
			},
			'g2e-confirm-pert': {
				key: 'perturbation',
				prompt: 'Please enter perturbation:'
			}
		},

		steps, $overlay, $modal, $progress, $results;

	app.ui.on_open_app = function() {
		var scraped_data;
		if (first_click) {
			app.ui.__setup();		
			// Prevent re-adding the modal box to the DOM.
			first_click = false;
		}

		// Show the user the data we have scraped for confirmation.
		scraped_data = app.scraper.scrape_data($modal);
		if (app.scraper.is_valid_data(scraped_data)) {
			app.ui.fill_confirm_tbl(scraped_data);
			app.ui.__show_modal_box();
		}
	};

	app.ui.__setup = function() {
		app.ui.__set_global_selectors();

		// Allow editing of the values, in case we scraped incorrectly.
		$('.g2e-edit').click(function(evt) {
			var id = $(evt.currentTarget).siblings().eq(1).attr('id');
			app.ui.__on_edit(id);
		});

		// Add event handlers
		$modal.find('#g2e-close-btn')
			  .click(app.ui.__reset_ui)
			  .end()

			  .find('#g2e-submit-btn')
			  .click(function() {
			      app.notifier.log('Input data was scraped');
			      app.notifier.log(app.scraper.get_data($modal));
			      app.comm.fetch_diffexp_enrich($modal);
			  })
			  .end()

			  .find('#g2e-download-btn')
			  .click(app.comm.download_diff_exp_files);
	};

	app.ui.show_progress_bar = function() {
		steps = ['#g2e-step1', '#g2e-step2', '#g2e-step3', '#g2e-step4'];
		$progress.show();
	};

	app.ui.highlight_next_step = function() {
		$progress.find(steps.shift()).addClass('g2e-ready');
	};

	// `app.scraper` also calls this when new data is set.
	app.ui.fill_confirm_tbl = function(scraped_data) {
		var elem, config, html;
		for (elem in elem_config) {
			config = elem_config[elem];
			if (config.format) {
				html = config.format(scraped_data[config.key]);
			} else {
				html = scraped_data[config.key];
			}
			$('#' + elem).html(html);
		}
	};

	app.ui.show_results = function(link) {
		$results.show()
				.find('button')
				.first()
				.click(function() {
					window.open(link, '_blank');
				});
	};

	app.ui.__hide_results = function() {
		$results.hide()
				.find('button')
				.first()
				.unbind();
	};

	app.ui.__show_modal_box = function() {
		$overlay.show();
		$modal.show();
	};

	app.ui.__hide_modal_box = function() {
		$overlay.hide();
		$modal.hide();
	};

	app.ui.__set_global_selectors = function() {
		var html = app.html.get('modal');
		$overlay = $(html).hide().appendTo('body');
		$modal = $('#g2e-container #g2e-modal').draggable();
		$progress = $progress || $('#g2e-progress-bar');
		$results = $results || $('#g2e-results');		
	}

	app.ui.__reset_ui = function() {
		app.ui.__hide_modal_box();
		$progress.hide()
				 .find('.g2e-progress')
				 .removeClass('g2e-ready');
		app.ui.__hide_results();
		app.comm.reset_downloaded_file();
		// TODO: A global switch that kills the requests?
		//app.global.make_requests = false;
	};

	app.ui.__on_edit = function(id) {
		var config = elem_config[id],
			user_input = app.notifier.prompt(config.prompt, $('#' + id).text());
		if (user_input !== null) {
			app.scraper.set_data(config.key, user_input);
		}
	};

})(GEO2Enrichr, jQuery);