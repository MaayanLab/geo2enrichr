
function UserInputHandler(comm, events, notifier, screenScraper, tagger) {

    var geneList;
    events.on('geneListFetched', function(data) {
        geneList = data;
    });

    function sendDataToServer($modalBox) {
        var selectedData = getData($modalBox);
        if (isValidData(selectedData)) {

            var data = {};
            for (var prop1 in selectedData.scrapedData) {
                data[prop1] = selectedData.scrapedData[prop1];
            }
            for (var prop2 in selectedData.userOptions) {
                data[prop2] = selectedData.userOptions[prop2];
            }

            data.metadataTags = {};
            for (var prop3 in selectedData.crowdsourcedMetadata) {
                data.metadataTags[prop3] = selectedData.crowdsourcedMetadata[prop3];
            }

            comm.postSoftFile(data);

            events.fire('dataPosted');
        }
    }

    function getData($modalBox) {
        return {
            scrapedData: screenScraper.getDataFromPage(),
            userOptions: getUserOptions($modalBox),
            crowdsourcedMetadata: getCrowdsourcedMetadata()
        };
    }

    function isValidData(data) {
        var selectedTags = tagger.getSelectedTags();
        if (!data.scrapedData.A_cols || data.scrapedData.A_cols.length < 2) {
            notifier.warn('Please select 2 or more control samples');
            return false;
        }
        if (!data.scrapedData.B_cols || data.scrapedData.B_cols.length < 2) {
            notifier.warn('Please select 2 or more experimental samples');
            return false;
        }
        // * WARNINGS *
        // It is important to verify that the user has *tried* to select a gene before warning them.
        // $.inArray() returns -1 if the value is not found. Do not check for truthiness.
        if (geneList && data.userOptions.gene && $.inArray(data.userOptions.gene, geneList) === -1) {
            notifier.warn('Please input a valid gene.');
            return false;
        }

        for (var tag in selectedTags) {
            for (var field in selectedTags[tag]) {
                var conf = selectedTags[tag][field];
                if (conf.required) {
                    debugger;
                }
            }
        }

        return true;
    }

    function getUserOptions($modalBox) {

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
        $('#required-fields-based-on-tag').find('tr').each(function(i, tr) {
            var $tr = $(tr);
            if ($tr.find('input').attr('required') === 'true') {
                debugger;
            } else {
                debugger;
            }
        });
        return {};
    }

    return {
        getData: getData,
        sendDataToServer: sendDataToServer
    };
}