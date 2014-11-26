var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.ui = {};

	var first_click = true,
		steps,
		$overlay, $modal, $progress;

	app.ui.on_click = function() {
		if (first_click) {
			app.ui.__setup();		
			// Prevent re-adding the modal box to the DOM.
			first_click = false;
		}
		
		// Show the user the data we have scraped for confirmation.
		scraped_data = app.scraper.scrape_data($modal);
		app.ui.fill_confirm_tbl(scraped_data);

		app.ui.__show_modal_box();
	};

	app.ui.__setup = function() {
		var html = app.html.get('modal'),
			scraped_data;

		$overlay = $(html).hide().appendTo('body');
		$modal = $('#g2e-container #g2e-modal').draggable();
		
		// Allow editing of the values, in case we scraped incorrectly.
		$('.g2e-edit').click(function(evt) {
			var id = $(evt.currentTarget).siblings().eq(1).attr('id');
			app.ui.__on_edit(id);
		});

		// Add event handlers
		$modal.find('#g2e-close-btn').click(function() {
			app.ui.__hide_modal_box();
			app.ui.__reset_ui();
		});
		$modal.find('#g2e-submit-btn').click(function() {
			app.comm.submit_data_to_enrich($modal);
		});
		$modal.find('#g2e-download-btn').click(app.comm.download_diff_exp_files);
	};

	app.ui.__show_modal_box = function() {
		$overlay.show();
		$modal.show();
	};

	app.ui.__hide_modal_box = function() {
		$overlay.hide();
		$modal.hide();
	};

	app.ui.__on_edit = function(id) {

		var id2Config = {
			'g2e-confirm-tbl-acc'  : {
				key: 'accession_num',
				prompt: 'Please enter a accession number:'
			},
			'g2e-confirm-tbl-pltf' : {
				key: 'platform',
				prompt: 'Please enter a platform:'
			},
			'g2e-confirm-tbl-spcs' : {
				key: 'species',
				prompt: 'Please enter a species:'
			},
			'g2e-confirm-tbl-ctrl' : {
				key: 'control',
				prompt: 'Please enter a comma-separated list of samples:'
			},
			'g2e-confirm-tbl-expmt': {
				key: 'experimental',
				prompt: 'Please enter a comma-separated list of samples:'
			}
		};

		var conf = id2Config[id],
			user_input = app.notifier.prompt(conf.prompt, $('#' + id).text());

		if (user_input !== null) {
			app.scraper.set_data(conf.key, user_input);
		}
	};

	app.ui.fill_confirm_tbl = function(scraped_data) {
		$('#g2e-confirm-tbl-acc').html(scraped_data.accession_num);
		$('#g2e-confirm-tbl-pltf').html(scraped_data.platform);
		$('#g2e-confirm-tbl-spcs').html(scraped_data.species);
		$('#g2e-confirm-tbl-ctrl').html(scraped_data.control);
		$('#g2e-confirm-tbl-expmt').html(scraped_data.experimental);
	};

	app.ui.show_progress_bar = function() {
		$progress = $progress || $('#g2e-progress-bar');
		app.ui.set_steps();
		$progress.show();
		app.ui.highlight_next_step();
	};

	app.ui.highlight_next_step = function() {
		$progress.find(steps.shift()).css({
			'background': '#FFC0CB',
			'color': '#000'
		});
	};

	app.ui.set_steps = function() {
		steps = ['#g2e-step1', '#g2e-step2', '#g2e-step3', '#g2e-step4'];
	};

	app.ui.handle_enrichr_links = function(links) {
		/*$.each(data.links, function(i, link) {
			window.open(link);
		});*/

		// TODO: If approved, move the HTML into html.js.
		if (links && links.length > 0) {
			if (links.length === 1) {
				$('#g2e-progress-bar').append('' +
					'<h4>Your links to Enrichr:</h4>' +
					'<a href="' + links[0] + '">Up or down genes</a>'
				);
			} else if (links.length === 2) {
				$('#g2e-progress-bar').append('' +
					'<h4>Your links to Enrichr:</h4>' +
					'<a href="' + links[0] + '" target="_blank">Up genes</a>' +
					'<a href="' + links[1] + '" target="_blank">Down genes</a>'
				);
			}
		}
	};

	app.ui.__reset_ui = function() {
		$progress = $progress || $('#g2e-progress-bar');
		$progress.hide();
		app.ui.set_steps();

		// TODO: A global switch that kills the requests?
		//app.global.make_requests = false;
	};

})(GEO2Enrichr, jQuery);