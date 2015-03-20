
var Ui = function(comm, events, notifier, scraper, SUPPORTED_PLATFORMS, targetApps, templater) {

    var geneList, $overlay, $resultsBtn, $submitBtn;

    // This function is called every time the "Pipe to Enrichr" button is clicked.
    var openModalBox = function() {
        var scrapedData = scraper.getScrapedData($overlay);
        fillConfirmationTable(scrapedData);
        $overlay.show();
    };

    var showResultsLink = function(extractionId) {
        $resultsBtn.show().click(function() {
            window.open(extractionId, "_blank");
        });
    };

    var resetModalBox = function() {
        resetFooter();
        $overlay.hide();
    };

    var resetFooter = function() {
        $resultsBtn.hide().off();
        $submitBtn.removeClass('g2e-lock').off().click(postData);
    };

    var postData = function() {
        var scrapedData = scraper.getScrapedData($overlay),
            userOptions = scraper.getUserOptions($overlay),
            data = $.extend({}, scrapedData, userOptions),
            app = targetApps.current();
        if (isValidData(scrapedData)) {
            $(this).addClass('g2e-lock').off();
            comm.postSoftFile(scrapedData, app);
        } else {
            resetFooter();
        }
    };

    var fillConfirmationTable = function(scrapedData) {
        var prop, html, elemId;
        for (prop in scrapedData) {
            var val = scrapedData[prop];
            if ($.isArray(val)) {
                html = val.join(', ');
            } else {
                html = val;
            }
            $('#g2e-' + prop + ' td').eq(1).html(html);
        }
    };

    var isValidData = function(data) {
        if (!data.A_cols || data.A_cols.length < 2) {
            notifier.warn('Please select 2 or more control samples');
            return false;
        }
        if (!data.B_cols || data.B_cols.length < 2) {
            notifier.warn('Please select 2 or more experimental samples');
            return false;
        }
        // * WARNINGS *
        // It is important to verify that the user has *tried* to select a gene before warning them.
        // $.inArray() returns -1 if the value is not found. Do not check for truthiness.
        if (geneList && data.gene && $.inArray(data.gene, geneList) === -1) {
            notifier.warn('Please input a valid gene.');
            return false;
        }
        return true;
    };

    var setAutocomplete = function(elemName, data) {
        $overlay.find(elemName).autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(data, request.term);
                response(results.slice(0, 10));
            },
            minLength: 2,
            delay: 250,
            autoFocus: true
        });
    };

    events.on('bootstrapped', function() {
        var $g2eLink =  $('#g2e-embedded-button #g2e-link'),
            platform = scraper.getPlatform();

        /* SUPPORTED_PLATFORMS is a global variable built by the deployment
         * script. We do this because (1) the array is small and can be loaded
         * into the client's memory; (2) any network, if the array was fetched
         * from the server, would erroneously tell the client we support that
         * platform; and (3) manually updating this variable in JS is easy to
         * forget.
         */
        if (platform && $.inArray(platform, SUPPORTED_PLATFORMS) === -1) {
            $g2eLink.html('<strong class="g2e-strong">G2E:</strong> This platform is not currently supported.');
        } else {
            $g2eLink.click(openModalBox);
        }
    });

    events.on('requestFailed', function(errorData) {
        notifier.warn(errorData.message);
        resetFooter();
    });

    events.on('geneListFetched', function(geneList) {
        setAutocomplete('#g2e-geneList', geneList);
    });

    events.on('resultsReady', showResultsLink);

    var init = (function() {
        var html = templater.get('modal');
        $(html).hide().appendTo('body');
        $('#g2e-modal').draggable();
        $overlay = $('#g2e-overlay');
        $resultsBtn = $overlay.find('#g2e-results-btn');
        $submitBtn = $overlay.find('#g2e-submit-btn').click(postData);
        $overlay.find('#g2e-close-btn').click(resetModalBox);
    })();
};
