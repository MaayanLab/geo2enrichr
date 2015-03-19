
var Ui = function(comm, events, notifier, scraper, SUPPORTED_PLATFORMS, targetApps, templater) {

    var $downloadIframe = $('<iframe>', { id: 'g2e-dl-iframe' }).hide().appendTo('body');
   
    var dataConfig = {
        'g2e-accession': {
            key: 'accession',
            prompt: 'Please enter an accession number:'
        },
        'g2e-platform': {
            key: 'platform',
            prompt: 'Please enter a platform:'
        },
        'g2e-organism' : {
            key: 'organism',
            prompt: 'Please enter an organism:'
        },
        'g2e-control': {
            key: 'A_cols',
            formatter: function(data) {
                return data.join(', ');
            }
        },
        'g2e-experimental': {
            key: 'B_cols',
            formatter: function(data) {
                return data.join(', ');
            }
        }
    };
    
    var geneList, $overlay, $modal, $results;

    // This is called once at startup. All variables and bindings should be permanent.
    var init = function() {
        $modal = templater.get('modal');
        $overlay = $modal.hide().appendTo('body');
        $('#g2e-container #g2e-modal').draggable();
        $results = $results || $('#g2e-results');

        // Allow editing of the values, in case we scraped incorrectly.
        $('.g2e-editable').click(function(evt) {
            var id = $(evt.target).parent().attr('id');
            onEdit(id);
        });

        // Add event handlers
        $modal.find('#g2e-target-app-select')
              .change(changeTargetApp)
              .end()
              .find('#g2e-close-btn')
              .click(resetModalBox)
              .end()
              .find('.g2e-confirm-tbl')
              .eq(1)
              .end();

        resetSubmitBtn();
    };

    var changeTargetApp = function(data) {
        // This is a great example of jQuery spaghetti. It would be much better to
        // have a model just back this view.
        targetApps.set( $(data.target).val() );
        $modal
            .find('#g2e-target-app-title')
            .text(targetApps.current().name)
            .css('color', targetApps.current().color);
        resetFooter(); 
    };

    // This function is called every time the "Pipe to Enrichr" button is clicked.
    var openModalBox = function() {
        var scrapedData;
        // Show the user the data we have scraped for confirmation.
        scrapedData = scraper.getData($modal);
        fillConfirmationTable(scrapedData);
        $overlay.show();
        $modal.show();
    };

    var setDownloadLinks = function(extractionId) {
        $results.find('#g2e-extract-link a').attr('href', extractionId);
        $results.show();
    };

    var showResults = function(data) {
        targetApps.current().resultsFormatter(data);
        $results.show();
    };

    var resetModalBox = function() {
        resetFooter();
        $overlay.hide();
        $modal.hide();
    };

    var resetFooter = function() {
        // Result any results.
        $('#g2e-target-app-results').remove();
        $results.hide()
                .find('button')
                .unbind();

        resetSubmitBtn();   
    };

    var resetSubmitBtn = function() {
        // Reset submit button.
        $modal.find('#g2e-submit-btn')
              // This doesn't do anything the first time.
              .removeClass('g2e-lock')
              // Remove any event handlers, just to be safe.
              // This code smells like jQuery spaghetti.
              .off()
              .click(function() {
                  var scrapedData = scraper.getData($modal),
                      app = targetApps.current();
                  if (isValidData(scrapedData)) {
                      $(this).addClass('g2e-lock').off();
                      comm.downloadDiffExp(scrapedData, app);
                  } else {
                      resetFooter();
                  }
              })
              .end();
    };

    var onEdit = function(id) {
        var config = dataConfig[id],
            userInput = notifier.ask(config.prompt, $('#' + id + ' td').eq(1).text()),
            newData;
        if (userInput !== null) {
            scraper.setData(config.key, userInput);
            newData = scraper.getData();
            fillConfirmationTable(newData);
        }
    };

    var fillConfirmationTable = function(scrapedData) {
        var elem, config, html;
        for (elem in dataConfig) {
            config = dataConfig[elem];
            if (config.formatter) {
                html = config.formatter(scrapedData[config.key]);
            } else {
                html = scrapedData[config.key];
            }
            $('#' + elem + ' td').eq(1).html(html);
        }
    };

    var downloadUrl = function(url) {
        $downloadIframe.attr('src', url);
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
        $modal.find(elemName).autocomplete({
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
            $g2eLink.html('<strong class="g2e-strong">GEOX:</strong> This platform is not currently supported.');
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

    events.on('rareDiseasesFetched', function(diseaseList) {
        setAutocomplete('#g2e-diseaseList', diseaseList);
    });

    events.on('dataReady', setDownloadLinks);

    events.on('genesEnriched', showResults);
    
    init();

    return {
        openModalBox: openModalBox
    };
};
