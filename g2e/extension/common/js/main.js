
var main = function() {
    
    var events = Events(),
        page = Page();

    if (page.isDataset()) {
        ScreenScraper(events, page, SUPPORTED_PLATFORMS, function(screenScraper) {

            //events, page, screenScraper, templater
            var notifier = Notifier(DEBUG),
                templater = Templater(IMAGE_PATH),
                uiEmbedder = UiEmbedder(events, page, screenScraper, templater),
                tagger,
                comm,
                eUtilsApi,
                userInputHandler;

            if (screenScraper.isSupportedPlatform()) {
                tagger = Tagger(events, templater);
                comm =  Comm(events, LoadingScreen, notifier, SERVER);
                eUtilsApi = EUtilsApi(comm, events, page, screenScraper);

                eUtilsApi.init();
                uiEmbedder.embed();
                userInputHandler = UserInputHandler(comm, events, notifier, screenScraper, tagger);
                ModalBox(events, tagger, templater, userInputHandler);

                events.fire('g2eLoaded');
            } else {
                uiEmbedder.abort();

            }
        });
    }
};