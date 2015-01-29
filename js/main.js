var main = function() {

    // EXTENSION_ID, DEBUG, and SERVER are set in config.js via deploy.sh.
    var events = Events(),
        notifier = Notifier(DEBUG),
        targetApps = TargetApps(events),
        templater = Templater(EXTENSION_ID, targetApps),
        baseScraper = BaseScraper(DEBUG),
        bootstrapper = Bootstrapper(events, notifier, templater),
        scraper,
        ui,
        comm;

    if (bootstrapper.isGds()) {
        modeScraper = GdsScraper(events);
    } else {
        modeScraper = GseScraper(events, templater);
    }

    scraper = $.extend(modeScraper, baseScraper);
    comm = Comm(events, notifier, targetApps, SERVER);
    ui = Ui(comm, events, notifier, scraper, targetApps, templater);
    
    bootstrapper.init();
    notifier.log('g2e loaded.');
};
