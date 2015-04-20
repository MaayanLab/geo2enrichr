
var Templater = function(IMAGE_PATH) {

    console.log(IMAGE_PATH);

    var modal = '' +
        '<div id="g2e-overlay">' +
            '<div id="g2e-modal">' +
                '<div id="g2e-title">' +
                    '<a href="http://amp.pharm.mssm.edu/g2e/" target="_blank">' +
                        '<img src="' + IMAGE_PATH + '">' +
                        '<span>GEO2</span>' +
                        '<span id="g2e-target-app">Enrichr</span>' +
                    '</a>' +
                '</div>' +
                '<div id="g2e-nav">' +
                    '<button id="g2e-close-btn" class="g2e-btn">&#10006</button>' +
                '</div>' +
                '<div class="g2e-clear"></div>' +
                '<table id="g2e-main-tbl">' +
                    '<tr>' +
                        '<td id="g2e-confirm">' +

                            '<div class="g2e-lowlight g2e-bottom">Please verify that your data is correct.</div>' +
                            '<table class="g2e-confirm-tbl">' +
                                '<tr id="g2e-dataset">' +
                                    '<td class="g2e-title">Accession num.</td>' +
                                    '<td class="g2e-value"></td>' +
                                '</tr>' +
                                '<tr id="g2e-platform">' +
                                    '<td class="g2e-title">Platform</td>' +
                                    '<td class="g2e-value"></td>' +
                                '</tr>' +
                                '<tr id="g2e-organism">' +
                                    '<td class="g2e-title">Organism</td>' +
                                    '<td class="g2e-value"></td>' +
                                '</tr>' +
                                '<tr id="g2e-A_cols">' +
                                    '<td class="g2e-title">Control samples</td>' +
                                    '<td class="g2e-value"></td>' +
                                '</tr>' +
                                '<tr id="g2e-B_cols" class="g2e-last">' +
                                    '<td class="g2e-title">Treatment or condition samples</td>' +
                                    '<td class="g2e-value"></td>' +
                                '</tr>' +
                            '</table>' +

                            '<div class="g2e-lowlight g2e-bottom">Please select differential expression analysis options.</div>' +
                            '<table class="g2e-confirm-tbl">' +
                                '<tr id="g2e-diffexp">' +
                                    '<td class="g2e-title">' +
                                        'Differential expression method' +
                                    '</td>' +
                                    '<td class="g2e-value g2e-select">' +
                                        '<select>' +
                                            '<option value="chdir">Characteristic direction</option>' +
                                            '<option value="ttest">T-test</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-normalize">' +
                                    '<td class="g2e-title">' +
                                        'Log-transform and quantile normalize if necessary&#42;' +
                                    '</td>' +
                                    '<td class="g2e-value g2e-select">' +
                                        '<select>' +
                                            '<option value="True">Yes</option>' +
                                            '<option value="False">No</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-cutoff">' +
                                    '<td class="g2e-title">' +
                                        'Cutoff' +
                                    '</td>' +
                                    '<td class="g2e-value g2e-select">' +
                                        '<select>' +
                                            '<option value="500">500</option>' +
                                            '<option value="1000">1000</option>' +
                                            '<option value="200">200</option>' +
                                            //'<option value="None">None</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +

                                '<tr id="g2e-correction-method" class="g2e-ttest">'+
                                    '<td class="g2e-title">' +
                                        'Correction method' +
                                    '</td>' +
                                    '<td class="g2e-value g2e-select">' +
                                        '<select>' +
                                            '<option value="BH">Benjamini-Hochberg</option>' +
                                            '<option value="bonferroni">Bonferroni</option>' +
                                            //'<option value="none">None</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-threshold" class="g2e-ttest">' +
                                    '<td class="g2e-title">' +
                                        'Threshold' +
                                    '</td>' +
                                    '<td class="g2e-value g2e-select">' +
                                        '<select name="threshold">' +
                                            '<option value="0.01">0.01</option>' +
                                            '<option value="0.05">0.05</option>' +
                                            //'<option value="none">None</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +

                            '<div class="g2e-lowlight g2e-bottom">Please fill out these optional annotations.</div>' +
                            '<table class="g2e-confirm-tbl">' +
                                '<tr id="g2e-cell">' +
                                    '<td class="g2e-title">' +
                                        'Cell type or tissue' +
                                    '</td>' +
                                    '<td class="g2e-value">' +
                                        '<input placeholder="No data">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-perturbation">' +
                                    '<td class="g2e-title">' +
                                        'Perturbation' +
                                    '</td>' +
                                    '<td class="g2e-value">' +
                                        '<input placeholder="No data">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-gene" class="ui-widget">' +
                                    '<td class="g2e-title">' +
                                        '<label for="g2e-geneList">Manipulated gene</label>' +
                                    '</td>' +
                                    '<td class="g2e-value">' +
                                        '<input id="g2e-geneList" placeholder="No data">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-disease" class="ui-widget g2e-last">' +
                                    '<td class="g2e-title">' +
                                        '<label for="g2e-diseaseList">Relevant disease</label>' +
                                    '</td>' +
                                    '<td class="g2e-value g2e-last">' +
                                        '<input id="g2e-diseaseList" placeholder="No data">' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +
                        '</td>' +
                    '</tr>' +
                '</table>' +
                '<div id="g2e-extract">' +
                    '<button id="g2e-submit-btn" class="g2e-btn">Extract gene lists</button>' +
                    '<button id="g2e-results-btn" class="g2e-btn">Open results tab</button>' +
                    '<p id="g2e-error-message" class="g2e-highlight">Unknown error. Please try again later.</p>' +
                '</div>' +
                '<div id="g2e-footer">' +
                    '<p id="g2e-credits">' + 
                        '&#42;See the <a href="http://amp.pharm.mssm.edu/g2e/#pipeline" target="_blank">website</a> for details.<br>' +
                        'GEO2Enrichr is being developed by the <a href="http://icahn.mssm.edu/research/labs/maayan-laboratory" target="_blank">Ma\'ayan Lab</a>.' +
                    '</p>' +
                '</div>' +
            '</div>' +
        '</div>';

    var BUTTON_TEXT = 'Extract knowledge with <strong class="g2e-strong">GEO2Enrichr</strong>';

    var EMBED_BTN_ID ="g2e-embedded-button";

    var templates = {
        'modal': modal,
        'gds': {
            'btn': $('' +
                '<tr>' +
                    // "azline" comes from the GEO website.
                    '<td class="azline" id="' + EMBED_BTN_ID + '">' +
                        '<b>Step 4: </b>' +
                        '<span id="g2e-link">' + BUTTON_TEXT + '</span>' +
                        '<img src="' + IMAGE_PATH + '">' +
                    '</td>' +
                '</tr>')
        },
        'gse': {
            'btn': $('' +
                '<tr>' +
                    '<td id="' + EMBED_BTN_ID + '">' +
                        '<span id="g2e-link">' + BUTTON_TEXT + '</span>' +
                        '<img src="' + IMAGE_PATH + '">' +
                    '</td>' +
                '</tr>'),
            'thead': $('' +
                // TODO: Rename "table-title" to "title"
                '<tr valign="top" id="g2e-table-title">' +
                    '<td></td>' +
                    '<td></td>' +
                    '<td class="g2e-ctrl">Control</td>' +
                    '<td class="g2e-expmt">Experimental</td>' +
                '</tr>'),

            'chkbxs': '' +
                '<td>' +
                    '<input class="g2e-chkbx g2e-control" type="checkbox" />' +
                '</td>' +
                '<td>' +
                    '<input class="g2e-chkbx g2e-experimental" type="checkbox" />' +
                '</td>'
        }
    };

    return {
        get: function(el, key) {
            if (key) {
                return templates[key][el];
            }
            return templates[el];
        },
        embedBtnId: function() {
            return EMBED_BTN_ID;
        }
    };
};
