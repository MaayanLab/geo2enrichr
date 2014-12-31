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
		var // Set these configuration values before deploying.

			// Production
            //EXTENSION_ID = 'pcbdeobileclecleblcnadplfcicfjlp',
			//DEBUG = false,
			//SERVER = 'http://amp.pharm.mssm.edu/',
			// Development
			EXTENSION_ID = 'jmocdkgcpalhikedehcdnofimpgkljcj',
			DEBUG = true,
			SERVER = 'http://localhost:8083/',

			events = Events(),
			notifier = Notifier(DEBUG),
			html = Html(EXTENSION_ID),
			baseScraper = BaseScraper(DEBUG, events, notifier),
			scraper,
			ui,
			comm;

		if (isGds()) {
			modeScraper = GdsScraper(events);
			scraper = $.extend(modeScraper, baseScraper);
			comm = Comm(events, notifier, scraper, SERVER);
			ui = $.extend(GdsUi(html, events), BaseUi(comm, events, html, notifier, scraper));
		} else {
			modeScraper = GseScraper(events, html);
			scraper = $.extend(modeScraper, baseScraper);
			comm = Comm(events, notifier, scraper, SERVER);
			ui = $.extend(GseUi(html, events), BaseUi(comm, events, html, notifier, scraper));
		}

		// This executes in the background, collecting information about the page before the user even inputs.
		if (scraper.getAccessionFromUrl) {
			comm.fetchMetadata(scraper.getAccessionFromUrl());
		}

		// Fetch and store the gene map for later.
		comm.fetchGenemap();
		ui.init();
		notifier.log('g2e loaded.');
	};

	init();
};
