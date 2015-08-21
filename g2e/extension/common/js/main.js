var main = function() {

    /* EXTENSION_ID, DEBUG, SERVER, and SUPPORTED_PLATFORMS are set in
     * config.js via build.sh.
     */
    var events = Events(),
        notifier = Notifier(DEBUG),
        templater = Templater(IMAGE_PATH),
        loader = Loader(),
        tagger = Tagger(events, templater),
        baseScraper = BaseScraper(DEBUG),
        bootstrapper = Bootstrapper(events, notifier, templater),
        scraper,
        ui,
        comm;

    /* TODO:
     * The Scraper--a class that doesn't exist--constructor should consume
     * the bootstrapper, discover what site it is on, and return the
     * appropriate constructor. main.js should not know about this.
     */
    var isGdsFl = bootstrapper.isGds();
    if (isGdsFl === 1) {
        modeScraper = GdsScraper(events);
    } else if (isGdsFl === -1) {
        modeScraper = GseScraper(events, templater);
    }

    scraper = $.extend(modeScraper, baseScraper);
    comm = Comm(events, loader, notifier, SERVER);
    ui = Ui(comm, events, notifier, scraper, SUPPORTED_PLATFORMS, tagger, templater);

    bootstrapper.init();
};
