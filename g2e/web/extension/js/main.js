var main = function() {

    var SUPPORTED_PLATFORMS = ['GPL8321', 'GPL7091', 'GPL3307', 'GPL8300', 'GPL11383', 'GPL13158', 'GPL4044', 'GPL1426', 'GPL6887', 'GPL3084', 'GPL32', 'GPL16268', 'GPL13692', 'GPL2881', 'GPL15207', 'GPL3697', 'GPL91', 'GPL339', 'GPL96', 'GPL17518', 'GPL15401', 'GPL13712', 'GPL201', 'GPL1261', 'GPL10558', 'GPL6193', 'GPL6244', 'GPL3050', 'GPL6101', 'GPL6885', 'GPL4685', 'GPL6102', 'GPL4200', 'GPL6480', 'GPL6106', 'GPL6845', 'GPL7202', 'GPL4134', 'GPL1708', 'GPL3921', 'GPL85', 'GPL4074', 'GPL2897', 'GPL4133', 'GPL6947', 'GPL1536', 'GPL1355', 'GPL4487', 'GPL81', 'GPL6096', 'GPL8063', 'GPL11202', 'GPL16686', 'GPL15792', 'GPL6246', 'GPL340', 'GPL11180', 'GPL13497', 'GPL571', 'GPL570'];
    
    /* EXTENSION_ID, DEBUG, SERVER, and SUPPORTED_PLATFORMS are set in
     * config.js via deploy.sh.
     */
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
    ui = Ui(comm, events, notifier, scraper, SUPPORTED_PLATFORMS, targetApps, templater);
    
    bootstrapper.init();
    notifier.log('g2e loaded.');
};
