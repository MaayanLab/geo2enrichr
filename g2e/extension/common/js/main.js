
var main = function() {

    var page = Page();

    if (page.isDataset()) {
        ScreenScraper(page, SUPPORTED_PLATFORMS, function(screenScraper) {
            if (screenScraper.isSupportedPlatform()) {

                var events = Events(),
                    notifier = Notifier(DEBUG),
                    templater = Templater(IMAGE_PATH),
                    tagger = Tagger(events, templater),
                    comm =  Comm(events, LoadingScreen, notifier, SERVER),
                    userInputHandler,

                    // TODO: Use this! It returns all the metadata we need.
                    eUtilsApi = EUtilsApi(comm, page, screenScraper);

                UiEmbedder(events, page, screenScraper, templater);
                userInputHandler = UserInputHandler(comm, events, notifier, screenScraper, tagger);
                ModalBox(events, tagger, templater, userInputHandler);

                events.fire('g2eLoaded');
            }
        });
    }
};