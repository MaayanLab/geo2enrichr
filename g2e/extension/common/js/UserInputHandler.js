
function UserInputHandler(comm, events, notifier, screenScraper, tagger) {

    var $modalBox,
        geneList,
        courseraUserKey = localStorage.getItem('g2e-submission-key');

    events.on('geneListFetched', function(data) {
        geneList = data;
    });

    events.on('g2eLoaded', function() {
        $modalBox.find('#g2e-user-key-wrapper input').change(function() {
            var newKey = $modalBox.find('#g2e-user-key').val();
            localStorage.setItem('g2e-submission-key', newKey);
        });
    });

    function setModalBox($el) {
        $modalBox = $el;
    }

    function sendDataToServer() {
        var selectedData = getData();
        if (isValidData(selectedData, false)) {
            selectedData = prepareForTransfer(selectedData);
            comm.postSoftFile(selectedData);
            events.fire('dataPosted');
        }
    }

    function prepareForTransfer(selectedData) {
        var result = {};

        $.each(selectedData.scrapedData, function(key, obj) {
            result[key] = obj;
        });

        $.each(selectedData.userOptions, function(key, obj) {
            result[key] = obj;
        });

        result.metadata = {};
        $.each(selectedData.crowdsourcedMetadata, function(key, obj) {
            result.metadata[key] = obj;
        });

        result.tags = selectedData.tags;

        return result;
    }

    function getData() {
        return {
            scrapedData: screenScraper.getDataFromPage(),
            userOptions: getUserOptions(),
            tags: tagger.getSelectedTags(),
            crowdsourcedMetadata: getCrowdsourcedMetadata()
        };
    }

    function isValidData(data, onlyCheckingIfProcessed) {
        var selectedTags = tagger.getSelectedTags(),
            tagsToFields = tagger.getTagsToFields(),
            checkForUser = false,
            tag,
            field,
            conf,
            selectedValue,
            key,
            i;

        if (notEnoughSamples(data.scrapedData.A_cols)) {
            notifier.warn('Please select 2 or more control samples');
            return false;
        }
        if (notEnoughSamples(data.scrapedData.B_cols)) {
            notifier.warn('Please select 2 or more experimental samples');
            return false;
        }
        if (isProperGeneSymbol(data.userOptions.gene)) {
            notifier.warn('Please input a valid gene.');
            return false;
        }

        if (!onlyCheckingIfProcessed) {
            // Use traditional for loops so we can exit early if necessary.
            for (i = 0; i < selectedTags.length; i++) {
                tag = selectedTags[i];
                for (field in tagsToFields[tag]) {
                    // If we reach this line of code, we need to verify the submission key.
                    checkForUser = true;
                    conf = tagsToFields[tag][field];
                    selectedValue = data.crowdsourcedMetadata[field];
                    if (conf.required && !selectedValue) {
                        notifier.warn('Please add metadata field "' + conf.description + '"');
                        return false;
                    }
                }
            }
            if (checkForUser) {
                if (keyDoesNotExist(data)) {
                    notifier.warn('Please add a submission key.');
                    return false;
                }
            }
        }

        return true;
    }

    function getUserOptions() {

        var data = {},
            method = $modalBox.find('#g2e-diffexp option:selected').val(),
            cutoff = $modalBox.find('#g2e-cutoff option:selected').val(),
            normalize = $modalBox.find('#g2e-normalize option:selected').val(),
            cell = $modalBox.find('#g2e-cell .g2e-value input').val(),
            perturbation = $modalBox.find('#g2e-perturbation .g2e-value input').val(),
            gene = $modalBox.find('#g2e-gene #g2e-geneList').val(),
            disease = $modalBox.find('#g2e-disease #g2e-diseaseList').val(),
            threshold = $modalBox.find('#g2e-threshold option:selected').val();

        if (method) {
            data.diffexp_method = method;
        }
        if (cutoff) {
            data.cutoff = cutoff;
        }
        if (normalize) {
            data.normalize = normalize;
        }
        if (cell) {
            data.cell = cell.replace(/_|\.|-/, '');
        }
        if (perturbation) {
            data.perturbation = perturbation.replace(/_|\.|-/, '');
        }
        if (gene) {
            data.gene = gene;
        }
        if (disease) {
            data.disease = disease;
        }
        if (threshold) {
            data.threshold = threshold;
        }

        return data;
    }

    /* August 2015:
     * Gets data from fields that are specific for the upcoming Coursera
     * MOOC. In principle, we can remove this in the future.
     */
    function getCrowdsourcedMetadata() {
        // I really hate how much this function knows about the DOM.
        var result = {},
            $table = $modalBox.find('#g2e-required-fields-based-on-tag'),
            key;
        $.each(tagger.getNewFields(), function(i, key) {
            var $input = $table.find('#' + key + ' input');
            if ($input.length) {
                result[key] = $input.val().replace(/ /g,'');
            }
        });

        key = $modalBox.find('#g2e-user-key').val() || courseraUserKey;
        if (key !== '') {
            result.user_key = key;
            localStorage.setItem('g2e-submission-key', key);
        }

        return result;
    }

    /* August 2015
     * Checks if data was processed for particular Coursera microtask. Can
     * also be deprecated in the future.
     */
    function checkIfProcessed() {
        var data = getData(),
            payload;
        if (data.tags.length != 1) {
            notifier.warn('Please check with only one tag.');
            return;
        }
        if (isValidData(data, true)) {
            payload = {
                geo_id: data.scrapedData.dataset,
                ctrl_ids: data.scrapedData.A_cols.join(','),
                pert_ids: data.scrapedData.B_cols.join(','),
                hashtag: '#' + data.tags[0]
            };

            comm.checkIfProcessed(payload, function(alreadyProcssed) {
                if (alreadyProcssed) {
                    notifier.warn('This combination of selected samples and tag has already been processed.');
                } else {
                    notifier.warn('This combination of selected samples and tag has *not* been processed.');
                }
            });
        }
    }

    /* Returns true if the user has selected fewer than 2 samples.
     */
    function notEnoughSamples(samples) {
        return typeof samples === 'undefined' || samples.length < 2;
    }

    /* Returns true if a gene symbol has been selected and is not in the list
     * of proper gene symbols.
     */
    function isProperGeneSymbol(gene) {
        // Do not check for truthiness: $.inArray() returns -1 if the value is
        // not found.
        return geneList && gene && $.inArray(gene, geneList) === -1;
    }

    /* Returns true if the user has not input a submission key.
     */
    function keyDoesNotExist(data) {
        var key = data.crowdsourcedMetadata.user_key;
        return typeof key === 'undefined' || key === '';
    }

    return {
        checkIfProcessed: checkIfProcessed,
        getData: getData,
        sendDataToServer: sendDataToServer,
        setModalBox: setModalBox
    };
}