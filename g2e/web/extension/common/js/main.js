var main = function() {

    /* EXTENSION_ID, DEBUG, SERVER, and SUPPORTED_PLATFORMS are set in
     * config.js via build.sh.
     */
    var events = Events(),
        notifier = Notifier(DEBUG),
        templater = Templater(IMAGE_PATH),
        baseScraper = BaseScraper(DEBUG),
        bootstrapper = Bootstrapper(events, notifier, templater),
        scraper,
        ui,
        comm;

    var isGdsFl = bootstrapper.isGds();
    if (isGdsFl === 1) {
        modeScraper = GdsScraper(events);
    } else if (isGdsFl === -1) {
        modeScraper = GseScraper(events, templater);
    }

    scraper = $.extend(modeScraper, baseScraper);
    comm = Comm(events, notifier, SERVER);
    ui = Ui(comm, events, notifier, scraper, SUPPORTED_PLATFORMS, templater);
    
    bootstrapper.init();
};
