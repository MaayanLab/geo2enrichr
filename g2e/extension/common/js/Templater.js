
var Templater = function(IMAGE_PATH) {

    var G2E_TITLE = 'g2e-title',
        G2E_VALUE = 'g2e-value',
        G2E_SELECT = 'g2e-select',
        G2E_TEXT = 'g2e-text';

    var modal = '' +
        '<div id="g2e-overlay">' +
            '<div id="g2e-modal">' +
                '<div id="' + G2E_TITLE + '">' +
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
                            '<table class="g2e-confirm-tbl g2e-top">' +
                                '<caption>Please verify that your data is correct.</caption>' +
                                '<tr id="g2e-dataset">' +
                                    '<td class="' + G2E_TITLE + '">Accession num.</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '"></td>' +
                                '</tr>' +
                                '<tr id="g2e-platform">' +
                                    '<td class="' + G2E_TITLE + '">Platform</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '"></td>' +
                                '</tr>' +
                                '<tr id="g2e-organism">' +
                                    '<td class="' + G2E_TITLE + '">Organism</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '"></td>' +
                                '</tr>' +
                                '<tr id="g2e-A_cols">' +
                                    '<td class="' + G2E_TITLE + '">Control samples</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '"></td>' +
                                '</tr>' +
                                '<tr id="g2e-B_cols" class="g2e-last">' +
                                    '<td class="' + G2E_TITLE + '">Treatment or condition samples</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '"></td>' +
                                '</tr>' +
                            '</table>' +
                            '<table class="g2e-confirm-tbl g2e-top">' +
                                '<caption>Please select differential expression analysis options.</caption>' +
                                '<tr id="g2e-diffexp">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Differential expression method' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + ' ' + G2E_SELECT + '">' +
                                        '<select>' +
                                            '<option value="chdir">Characteristic direction</option>' +
                                            '<option value="ttest">T-test</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-cutoff">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Cutoff' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + ' ' + G2E_SELECT + '">' +
                                        '<select>' +
                                            '<option value="500">500</option>' +
                                            '<option value="1000">1000</option>' +
                                            '<option value="200">200</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-correction-method" class="g2e-ttest">'+
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Correction method' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + ' ' + G2E_SELECT + '">' +
                                        '<select>' +
                                            '<option value="BH">Benjamini-Hochberg</option>' +
                                            '<option value="bonferroni">Bonferroni</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-threshold" class="g2e-ttest">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Threshold' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + ' ' + G2E_SELECT + '">' +
                                        '<select name="threshold">' +
                                            '<option value="0.01">0.01</option>' +
                                            '<option value="0.05">0.05</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-normalize">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Transform and normalize if necessary&#42;' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + ' ' + G2E_SELECT + '">' +
                                        '<select>' +
                                            '<option value="False">No</option>' +
                                            '<option value="True">Yes</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +
                            '<table id="g2e-metadata" class="g2e-confirm-tbl g2e-top">' +
                                '<caption>Please fill out these optional annotations.</caption>' +
                                '<tr id="g2e-cell">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Cell type or tissue' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '">' +
                                        '<input type="text" placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-perturbation">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Perturbation' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '">' +
                                        '<input type="text" placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-gene" class="ui-widget">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        '<label for="g2e-geneList">Manipulated gene</label>' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '">' +
                                        '<input type="text" id="g2e-geneList" placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-disease" class="ui-widget g2e-last">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        '<label for="g2e-diseaseList">Relevant disease</label>' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + ' g2e-last">' +
                                        '<input type="text" id="g2e-diseaseList" placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +
                            '<table class="g2e-confirm-tbl g2e-top">' +
                                '<caption>Please apply metadata tags.</caption>' +
                                '<tr id="g2e-cell">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Metadata Tags' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '">' +
                                        '<ul id="g2e-tags"></ul>' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +
                            '<div id="g2e-crowdsourcing-details" class="g2e-crowdsourcing g2e-hidden">' +
                                '<h1>Coursera Microtasks</h1>' +
                                '<div class="g2e-left">' +
                                    '<button>Check if already processed</button>' +
                                '</div>' +
                                '<div id="g2e-user-key-wrapper" class="g2e-left">' +
                                    '<label for="g2e-user-key">Submission Key ' +
                                        '<input id="g2e-user-key" text="text" class="' + G2E_TEXT + '">' +
                                    '</label>' +
                                '</div>' +
                            '</div>' +
                            '<table class="g2e-confirm-tbl g2e-crowdsourcing" id="g2e-required-fields-based-on-tag">' +
                                '<caption>Please fill out these required annotations.</caption>' +
                            '</table>' +
                        '</td>' +
                    '</tr>' +
                '</table>' +
                '<div id="g2e-extract">' +
                    '<div>' +
                        '<button id="g2e-submit-btn" class="g2e-btn">Extract gene lists</button>' +
                        '<button id="g2e-results-btn" class="g2e-btn">Open results tab</button>' +
                        '<p id="g2e-error-message" class="g2e-highlight">Unknown error. Please try again later.</p>' +
                    '</div>' +
                '</div>' +
                '<div id="g2e-footer">' +
                    '<p id="g2e-credits">' + 
                        '&#42;See the <a href="http://amp.pharm.mssm.edu/g2e/pipeline" target="_blank">website</a> for details.<br>' +
                        'GEO2Enrichr is being developed by the <a href="http://icahn.mssm.edu/research/labs/maayan-laboratory" target="_blank">Ma\'ayan Lab</a>.' +
                    '</p>' +
                '</div>' +
            '</div>' +
        '</div>';

    var BUTTON_TEXT = 'Extract knowledge with <strong class="g2e-strong">GEO2Enrichr</strong>';

    var EMBED_BTN_ID ="g2e-embedded-button";

    var templates = {
        modal: modal,
        gds: {
            openModalButton: $('' +
                '<tr>' +
                    // "azline" comes from the GEO website.
                    '<td class="azline" id="' + EMBED_BTN_ID + '">' +
                        '<b>Step 4: </b>' +
                        '<span id="g2e-link">' + BUTTON_TEXT + '</span>' +
                        '<img src="' + IMAGE_PATH + '">' +
                    '</td>' +
                '</tr>')
        },
        gse: {
            openModalButton: $('' +
                '<tr>' +
                    '<td id="' + EMBED_BTN_ID + '">' +
                        '<span id="g2e-link">' + BUTTON_TEXT + '</span>' +
                        '<img src="' + IMAGE_PATH + '">' +
                    '</td>' +
                '</tr>'),
            thead: $('' +
                // TODO: Rename "table-title" to "title"
                '<tr valign="top" id="g2e-table-title">' +
                    '<td></td>' +
                    '<td></td>' +
                    '<td class="g2e-ctrl">Control</td>' +
                    '<td class="g2e-expmt">Experimental</td>' +
                '</tr>'),

            checkboxes: '' +
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
        },
        getTableRow: function(value, id) {
            return $('' +
                '<tr id="' + id + '">' +
                    '<td class="' + G2E_TITLE + '">' + value + '</td>' +
                    '<td class="' + G2E_VALUE + ' ' + G2E_TEXT + '">' +
                        '<input placeholder="...">' +
                    '</td>' +
                '</tr>'
            );
        }
    };
};
