

var main = function() {

	var isGds = function() {
		var path;
		if (window.location.pathname !== '/') {
			path = window.location.pathname.split('/')[1];
			if (path === 'sites') {
				return true;
			} else if (path === 'geo') {
				return false;
			}
		}
	};

	var init = function() {
		// Set these configuration values before deploying.
		var DEBUG = false,
			SERVER = 'http://amp.pharm.mssm.edu/',

			events = Events(),
			notifier = Notifier(DEBUG),
			html = Html(),

			scraper,
			ui,
			comm;

		if (isGds()) {
			scraper = $.extend(GdsScraper(events), BaseScraper(notifier));
			comm = Comm(events, notifier, scraper, SERVER);
			ui = $.extend(GdsUi(html, events), BaseUi(comm, events, html, notifier, scraper));
		} else {
			scraper = $.extend(GseScraper(events, html), BaseScraper(notifier));
			comm = Comm(events, notifier, scraper, SERVER);
			ui = $.extend(GseUi(html, events), BaseUi(comm, events, html, notifier, scraper));
		}

		// This executes in the background, collecting information about the page before the user even inputs.
		if (scraper.getAccessionFromUrl) {
			comm.fetchMetadata( scraper.getAccessionFromUrl() );
		}

		// Fetch and store the gene map for later.
		comm.fetchGenemap();

		scraper.init();
		ui.init();
		notifier.log('g2e loaded.');
	};

	init();
};
