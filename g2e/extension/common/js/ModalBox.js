
/* The primary user interface, a single modal box.
 */
function ModalBox(events, tagger, templater, userInputHandler) {

    var $modalBox;
    (function init() {
        var html = templater.get('modal');
        $(html).hide().appendTo('body');
        $('#g2e-modal').draggable({
            cancel: '.g2e-text'
        });
        $modalBox = $('#g2e-overlay');
        $modalBox.find('#g2e-error-message').hide();
        $modalBox.find('#g2e-submit-btn').click(userInputHandler.sendDataToServer);
        $modalBox.find('#g2e-close-btn').click(function() {
            resetFooter();
            $modalBox.hide();
        });
        tagger.init(
            $modalBox.find("#g2e-tags"),
            $modalBox.find('#g2e-required-fields-based-on-tag')
        );
        $modalBox.find('#g2e-crowdsourcing-details button').click(function() {
            userInputHandler.checkIfProcessed();
        });

        userInputHandler.setModalBox($modalBox);
        setupDiffExpMethodOptions();
    })();

    events.on('openModalBox', openModalBox);

    events.on('geneListFetched', setAutocomplete);

    events.on('resultsReady', function(data) {
        $modalBox.find('g2e-lock').off();
        showResultsLink(data);
    });

    events.on('resultsError', function() {
        $modalBox.find('#g2e-error-message').show();
    });

    events.on('dataPosted', function() {
        $modalBox.find('#g2e-submit-btn').addClass('g2e-lock').off();
    });

    function openModalBox() {
        var data = userInputHandler.getData();
        fillConfirmationTable(data);
        $modalBox.show();
    }

    function showResultsLink(extractionId) {
        $modalBox.find('#g2e-results-btn').show().click(function() {
            window.open(extractionId, "_blank");
        });
    }

    function resetFooter() {
        $modalBox.find('#g2e-results-btn').hide().off();
        $modalBox.find('#g2e-submit-btn').removeClass('g2e-lock').off().click(userInputHandler.sendDataToServer);
        $modalBox.find('#g2e-error-message').hide();
    }

    function fillConfirmationTable(data) {
        var scrapedData = data.scrapedData,
            prop, html;
        for (prop in scrapedData) {
            var val = scrapedData[prop];
            if ($.isArray(val)) {
                html = val.join(', ');
            } else {
                html = val;
            }
            $('#g2e-' + prop + ' td').eq(1).html(html);
        }
        $modalBox.find('#g2e-user-key').val(data.crowdsourcedMetadata.user_key);
    }

    function setAutocomplete(data) {
        $modalBox.find('#g2e-geneList').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(data, request.term);
                response(results.slice(0, 10));
            },
            minLength: 2,
            delay: 250,
            autoFocus: true
        });
    }

    function setupDiffExpMethodOptions() {
        var $ttest = $('.g2e-ttest');
        var $cutoff = $('#g2e-cutoff');
        var $threshold = $('#g2e-threshold');
        $ttest.hide();
        $modalBox.find('#g2e-diffexp').change(function(evt) {
            var method = $(evt.target).val();
            if (method === 'chdir') {
                $cutoff.show();
                $ttest.hide();
            } else {
                $cutoff.hide();
                $ttest.show();
            }
        });
        $modalBox.find('#g2e-correction-method').change(function(evt) {
            var val = $(evt.target).val();
            if (val === 'none') {
                $threshold.hide();
            } else {
                $threshold.show();
            }
        });
    }
}