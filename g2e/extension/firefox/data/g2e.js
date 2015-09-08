
var G2E = (function() {

// This file is built by deploy.sh in the root directory.
var DEBUG = true;
var SERVER = "http://localhost:8083/g2e/";
var IMAGE_PATH = self.options.logoUrl;
// This file is built when new platforms are added.
//// We use an array rather than hitting an API endpoint because this is much
// faster. If the server is too slow, we will not notify the user that the
// platform is not supported in a timely fashion.
var SUPPORTED_PLATFORMS = ["GPL8321","GPL7091","GPL11383","GPL2902","GPL4044","GPL2700","GPL6887","GPL3084","GPL16268","GPL13692","GPL2881","GPL2011","GPL94","GPL15207","GPL3697","GPL2006","GPL93","GPL92","GPL339","GPL284","GPL6883","GPL17518","GPL887","GPL15401","GPL13712","GPL201","GPL1261","GPL10558","GPL6193","GPL6244","GPL3050","GPL7430","GPL6101","GPL6885","GPL95","GPL4685","GPL2507","GPL3408","GPL44","GPL6102","GPL4200","GPL6480","GPL6106","GPL7202","GPL4134","GPL1708","GPL3921","GPL85","GPL4074","GPL2897","GPL4133","GPL6947","GPL10666","GPL1536","GPL1355","GPL11532","GPL4487","GPL80","GPL81","GPL6096","GPL8063","GPL737","GPL11202","GPL16686","GPL15792","GPL6246","GPL340","GPL2895","GPL11180","GPL97","GPL13497","GPL571","GPL570"];


/* Communicates to external resources, such as G2E and Enrichr's APIs.
 */
var Comm = function(events, LoadingScreen, notifier, SERVER) {

    var loadingScreen = LoadingScreen('Processing data. This may take a minute.');

    /* An IIFE that fetches a list of genes from Enrichr for autocomplete.
     */
    (function fetchGeneList() {
        try {
            $.ajax({
                url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
                type: 'GET',
                dataType: 'JSON',
                success: function(data) {
                    events.fire('geneListFetched', data);
                }
            });
        } catch (err) {
        }
    })();

    /* POSTs user data to G2E servers.
     */
    function postSoftFile(inputData) {
        loadingScreen.start();
        $.post(SERVER + 'api/extract/geo',
            inputData,
            function(data) {
                if (!!data.error) {
                    events.fire('resultsError');
                } else {
                    var id = data.extraction_id,
                        url = SERVER + 'results/' + id;
                    events.fire('resultsReady', url);
                }
            })
            .fail(function(xhr, status, error) {
                events.fire('resultsError');
            })
            .always(function() {
                loadingScreen.stop();
            });
    }

    function checkIfProcessed(payload, callback) {
        loadingScreen.start();
        $.post(
            'http://maayanlab.net/crowdsourcing/check_geo.php',
            payload,
            function(response) {
                console.log(payload);
                callback(response === 'exist');
            })
            .error(function() {
                notifier.warn('Unknown error.');
            })
            .always(function() {
                loadingScreen.stop();
            });
    }

    return {
        checkIfProcessed: checkIfProcessed,
        postSoftFile: postSoftFile
    };
};


/* Checks which, if any, dataset page GEO2Enrichr is on.
 */
function Page() {

    var IS_DATASET_PAGE,
        IS_GDS_PAGE,
        path;

    (function findPage() {
        if (window.location.pathname !== '/') {
            path = window.location.pathname.split('/')[1];
            if (path === 'sites') {
                IS_DATASET_PAGE = true;
                IS_GDS_PAGE = true;
            } else if (path === 'geo') {
                IS_DATASET_PAGE = true;
                IS_GDS_PAGE = false;
            } else {
                IS_DATASET_PAGE = false;
            }
        }
    })();

    return {
        isDataset: function() {
            return IS_DATASET_PAGE;
        },
        isGds: function() {
            return IS_GDS_PAGE;
        }
    };
}

/* Embeds HTML into the page, depending on context.
 */
function UiEmbedder(events, page, screenScraper, templater) {

    (function embed() {
        var $modalButtonParent = screenScraper.getModalButtonParent();
        if (page.isGds()) {
            embedInGdsPage($modalButtonParent);
        } else {
            var $metadataTableParent = screenScraper.getMetadataTable();
            embedInGsePage($modalButtonParent, $metadataTableParent);
        }
    })();

    function embedInGsePage($modalButtonParent, $metadataTableParent) {
        var $openModalButtonHtml = templater.get('openModalButton', 'gse');
        $modalButtonParent.append($openModalButtonHtml);
        $openModalButtonHtml.click(function() {
            events.fire('openModalBox');
        });

        $metadataTableParent.find('tr').each(function(i, tr) {
            if ($(tr)
                .find('td')
                .first()
                .text()
                .toLowerCase()
                .indexOf('samples') === 0)
            {
                $samples_table = $(tr);
                return false;
            }
        });

        $samples_table
            .find('tr')
            .each(function(i, tr) {
                $(tr).append(templater.get('checkboxes', 'gse'));
            })
            .end()
            .find('table')
            .first()
            .find('tr')
            .first()
            .before(templater.get('thead', 'gse'));
    }

    function embedInGdsPage($modalButtonParent) {
        var $openModalButtonHtml = templater.get('openModalButton', 'gds');
        $modalButtonParent.children().last().after($openModalButtonHtml);
        $openModalButtonHtml.click(function() {
            events.fire('openModalBox');
        });
    }
}

var Events = function() {

	var channel = {};

	var fire = function(eventName, args) {
		if (!channel[eventName]) {
			return false;
		}
		var i = 0,
			len = channel[eventName].length;
		for (; i < len; i++) {
			channel[eventName][i](args);
		}
	};

	var on = function(eventName, callback) {
		if (!channel[eventName]) {
			channel[eventName] = [];
		}
		channel[eventName].push(callback);
	};

	return {
		on: on,
		fire: fire,
	};
};


/* Abstracts issues of adding new required fields depending on metadata. 95%
 * of this module is only required for a 2015 Coursera MOOC and could be
 * refactored once the course is over.
 *
 * https://www.coursera.org/course/bd2klincs
 */
var Tagger = function(events, templater) {

    var selectedTags = [],
        newFields = [],
        numCrowdsourcingTabs = 0,
        $table;

    var tagsToFields = {
        AGING_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            young: {
                required: true,
                description: "Age of the young sample"
            },
            old: {
                required: true,
                description: "Age of the old sample"
            },
            age_unit: {
                required: true,
                description: "Unit of age, choose among day, month, year"
            }
        },
        MCF7_BD2K_LINCS_DCIC_COURSERA: {
            pert_type: {
                required: true,
                description: "Perturbation type, choose among genetic, chemical, physical, other"
            },
            pert_name: {
                required: true,
                description: "Perturbagen name"
            },
            pert_id: {
                required: false,
                description: "Identifier of the perturbagen"
            }
        },
        DISEASES_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                "key": "",
                description: "Organism (human, mouse or rat)"
            },
            disease_name: {
                required: true,
                description: "Name of the disease"
            },
            disease_id: {
                required: true,
                description: "ID of the disease (from Disease-Ontology or UMLS)"
            }
        },
        LIGANDS_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            ligand_name: {
                required: true,
                description: "Name of the ligand"
            },
            ligand_id: {
                required: true,
                description: "Identifier of the ligand"
            }
        },
        DRUGS_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            drug_name: {
                required: true,
                description: "Name of the drug"
            },
            drug_id: {
                required: true,
                description: "ID of the Drug (from DrugBank or PubChem)"
            }
        },
        GENES_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            gene: {
                required: true,
                description: "Gene being perturbed in the study"
            },
            pert_type: {
                required: true,
                description: "Perturbation type (KO, KD, OE, Mutation)"
            }
        },
        PATHOGENS_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            microbe_name: {
                required: true,
                description: "Name of the virus or bacteria"
            },
            microbe_id: {
                required: false,
                description: "Taxonomy ID of the virus or bacteria"
            }
        }
    };

    function isCrowdsourcingTag(tag) {
        return typeof tagsToFields[tag] !== 'undefined';
    }

    function crowdsourcingTagAlreadyAdded() {
        return numCrowdsourcingTabs === 1;
    }

    /* Remove the hash on the tag if one exists.
     */
    function removeLeadingHash(tag) {
        if (hasLeadingHash(tag)) {
            return tag.slice(1);
        }
        return tag;
    }

    function hasLeadingHash(tag) {
        return tag.indexOf('#') === 0;
    }

    function isJustHash(tag) {
        return hasLeadingHash(tag) && tag.length === 1;
    }

    function addRequiredRows(newTag) {
        $.each(tagsToFields[newTag], function(key, newRow) {
            newFields.push(key);
            var $tr = templater.getTableRow(newRow.description, key);
            $table.append($tr);
        });
    }

    function removeUnrequiredRows(oldTag) {
        $.each(tagsToFields[oldTag], function(key) {
            var $oldRow = $('#' + key),
                idx = newFields.indexOf(key);
            if (idx > -1) {
                newFields.splice(idx, 1);
            }
            $oldRow.remove();
        });
    }

    function watch($input) {
        var $crowdsourcingElements = $('.g2e-crowdsourcing'),
            $metadataTable = $('#g2e-metadata');

        $input.tagit({
            singleField: true,
            caseSensitive: false,
            allowDuplicates: false,
            beforeTagAdded: function (evt, ui) {
                var newTag = $(ui.tag).find('.tagit-label').html();

                if (isJustHash(newTag)) {
                    return false;
                }

                newTag = removeLeadingHash(newTag);
                if (isCrowdsourcingTag(newTag) && crowdsourcingTagAlreadyAdded()) {
                    return false;
                }

                selectedTags.push(newTag);
                if (isCrowdsourcingTag(newTag)) {
                    addRequiredRows(newTag);
                    numCrowdsourcingTabs++;
                    $crowdsourcingElements.show();
                }
                if (numCrowdsourcingTabs > 0) {
                    $metadataTable.hide();
                }

                return newTag;
            },
            afterTagRemoved: function (evt, ui) {
                var oldTag = $(ui.tag).find('.tagit-label').html(),
                    idx;

                oldTag = removeLeadingHash(oldTag);
                idx = selectedTags.indexOf(oldTag);

                if (idx > -1) {
                    selectedTags.splice(idx, 1);
                }
                if (isCrowdsourcingTag(oldTag)) {
                    removeUnrequiredRows(oldTag);
                    numCrowdsourcingTabs--;
                    if (numCrowdsourcingTabs === 0) {
                        $crowdsourcingElements.hide();
                    }
                }
                if (numCrowdsourcingTabs === 0) {
                    $metadataTable.show();
                }
            }
        });
    }

    function init($input, $t) {
        $table = $t;
        watch($input);
    }

    return {
        init: init,
        getSelectedTags: function() {
            return selectedTags;
        },
        getNewFields: function() {
            return newFields;
        },
        getTagsToFields: function() {
            return tagsToFields;
        }
    };
};

var Templater = function(IMAGE_PATH) {

    var G2E_TITLE = 'g2e-title',
        G2E_VALUE = 'g2e-value';

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
                                    '<td class="' + G2E_VALUE + '"><input type="text"></td>' +
                                '</tr>' +
                                '<tr id="g2e-platform">' +
                                    '<td class="' + G2E_TITLE + '">Platform</td>' +
                                    '<td class="' + G2E_VALUE + '"><input type="text"></td>' +
                                '</tr>' +
                                '<tr id="g2e-organism">' +
                                    '<td class="' + G2E_TITLE + '">Organism</td>' +
                                    '<td class="' + G2E_VALUE + '"><input type="text"></td>' +
                                '</tr>' +
                                '<tr id="g2e-A_cols">' +
                                    '<td class="' + G2E_TITLE + '">Control samples</td>' +
                                    '<td class="' + G2E_VALUE + '"><input type="text"></td>' +
                                '</tr>' +
                                '<tr id="g2e-B_cols" class="g2e-last">' +
                                    '<td class="' + G2E_TITLE + '">Treatment or condition samples</td>' +
                                    '<td class="' + G2E_VALUE + '"><input type="text"></td>' +
                                '</tr>' +
                            '</table>' +
                            '<table class="g2e-confirm-tbl g2e-top">' +
                                '<caption>Please select differential expression analysis options.</caption>' +
                                '<tr id="g2e-diffexp">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Differential expression method' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' g2e-select">' +
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
                                    '<td class="' + G2E_VALUE + ' g2e-select">' +
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
                                    '<td class="' + G2E_VALUE + ' g2e-select">' +
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
                                    '<td class="' + G2E_VALUE + ' g2e-select">' +
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
                                    '<td class="' + G2E_VALUE + ' g2e-select">' +
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
                                    '<td class="' + G2E_VALUE + '">' +
                                        '<input placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-perturbation">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Perturbation' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + '">' +
                                        '<input placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-gene" class="ui-widget">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        '<label for="g2e-geneList">Manipulated gene</label>' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + '">' +
                                        '<input id="g2e-geneList" placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-disease" class="ui-widget g2e-last">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        '<label for="g2e-diseaseList">Relevant disease</label>' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + ' g2e-last">' +
                                        '<input id="g2e-diseaseList" placeholder="...">' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +
                            '<table class="g2e-confirm-tbl g2e-top">' +
                                '<caption>Please apply metadata tags.</caption>' +
                                '<tr id="g2e-cell">' +
                                    '<td class="' + G2E_TITLE + '">' +
                                        'Metadata Tags' +
                                    '</td>' +
                                    '<td class="' + G2E_VALUE + '">' +
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
                                        '<input id="g2e-user-key" text="text">' +
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
                    '<td class="' + G2E_VALUE + '">' +
                        '<input placeholder="...">' +
                    '</td>' +
                '</tr>'
            );
        }
    };
};


/* A simple loading screen with a configurable message.
 */
function LoadingScreen(message) {

    var $body = $('body'),
        $el = $('' +
            '<div class="g2e-loader-container">' +
                '<div class="g2e-loader-modal">' + message + '</div>' +
            '</div>'
        );

    return {
        start: function() {
            $body.append($el);
        },
        stop: function() {
            $el.remove();
        }
    };
}

var Notifier = function(DEBUG) {

	var log = function(msg) {
		if (DEBUG) {
			console.log(msg);
		}
	};

	var warn = function(msg) {
		alert(msg);
	};

	return {
		log: log,
		warn: warn
	};
};


/* Contains functions that are used on both GSE and GDS pages. The returned
 * object is a mixin of the general functionality with a context-dependent
 * scraper.
 */
function ScreenScraper(page, SUPPORTED_PLATFORMS, onConstructedCallback) {

    var modeScraper,
        $modalButtonParent,
        $metadataTableParent;

    var scraper = {

        getModalButtonParent: function() {
            return $modalButtonParent;
        },

        getMetadataTableParent: function () {
            return $metadataTableParent;
        },

        isSupportedPlatform: function() {
            var platform = this.getPlatform();
            // TODO: These two branches should be in an $.ajax callback.
            if (platform && $.inArray(platform, SUPPORTED_PLATFORMS) === -1) {
                return false;
            } else {
                return true;
            }
        },

        getDataFromPage: function() {
            var data = {},
                samples;
            samples = this.getSamples();
            data.A_cols = samples.A_cols;
            data.B_cols = samples.B_cols;
            data.dataset  = this.getDataset();
            data.organism = this.getOrganism();
            data.platform = this.getPlatform();
            return data;
        },

        textFromHtml: function($el) {
            if (!($el instanceof $)) {
                $el = $($el);
            }
            return $el.contents().filter(function() {
                return this.nodeType === 3;
            }).text().trim();
        },

        normalizeText: function(el) {
            return el.replace(/\s/g, '').toLowerCase();
        }
    };

    /* This function is async because GDS pages do not load all at once. This
     * Why the ScreenScraper constructor does not return an instance immediately.
     */
    (function getContextDependentScraper() {
        if (page.isGds()) {
            $metadataTableParent = $('#gds_details');
            var id = setInterval(function () {
                $modalButtonParent = $('#diff_express > tbody');
                if ($modalButtonParent.length) {
                    clearInterval(id);
                    modeScraper = GdsScraper($metadataTableParent, $modalButtonParent);
                    onConstructedCallback($.extend(modeScraper, scraper));
                }
            }, 50);
        } else {
            // Go up two parents to find the table.
            $modalButtonParent = $('#geo2r').next();
            // Find the details table based on its style attributes.
            $('table').each(function(i, table) {
                var $table = $(table);
                if ($table.attr('width') === '600' && $table.attr('cellpadding') === '2' && $table.attr('cellspacing') === '0') {
                    $metadataTableParent = $table;
                    return false;
                }
            });
            modeScraper = GseScraper($metadataTableParent);
            onConstructedCallback($.extend(modeScraper, scraper));
        }
    })();
}

var GdsScraper = function($metadataTableParent, $modalButtonParent) {

    return {

        getDataset: function() {
            var record_caption = $metadataTableParent.find('.caption').text(),
                re = new RegExp(/(?:GDS|GSE)[0-9]*/);
            return re.exec(record_caption)[0];
        },

        getOrganism: function() {
            return this.getByName('organism');
        },

        getPlatform: function() {
            return this.getByName('platform');
        },

        getSamples: function() {
            var $groupRow = $($modalButtonParent.children().find('tbody td')[0]),
                bkp_not_found = true,
                samplesStr = this.textFromHtml($groupRow),
                samplesArr = samplesStr.split(' '),
                samplesBkpIdx, A_cols, B_cols;

            $.each(samplesArr, function(i, val) {
                if (bkp_not_found && val.substr(val.length-1) !== ',') {
                    samplesBkpIdx = i+1;
                    bkp_not_found = false;
                } else {
                    // WARNING: we're mutating the list while iterating over it. 
                    // This should be okay since we're just trimming the comma.
                    samplesArr[i] = val.replace(',', '');
                }
            });

            return {
                A_cols: samplesArr.slice(0, samplesBkpIdx),
                B_cols: samplesArr.slice(samplesBkpIdx, samplesArr.length)
            };
        },

        getByName: function(name) {
            // 1. Grab the text from the appropriate row
            // 2. Strip out all the whitespace (newlines, tabs, etc.)
            // 3. Split on the semicolon (notice there are two) and return just the code.
            var idx = this.getRowIdxFromName(name);
            var text = $($metadataTableParent.find('tr')[idx]).text();
            // Remove any preceding whitespace.
            return text.split(':')[1].replace(/\s*/, '');
        },

        getRowIdxFromName: function(attrName) {
            var self = this,
                result;
            $metadataTableParent.find('tr').each(function(i, tr) {
                var titleEl = $(tr).find('th')[0],
                    titleText = self.normalizeText($(titleEl).text()),
                    titleName = titleText.split(':')[0];
                if (titleName === attrName) {
                    result = i;
                    return false;
                }
            });
            return result;
        }
    };
};


var GseScraper = function($metadataTableParent) {

    return {

        getByName: function(name) {
            var idx = this.getRowIdxByName(name);
            return $($metadataTableParent.find('tr')[idx]).find('a').text();
        },

        getRowIdxByName: function(attr_name) {
            var self = this,
                result;
            $metadataTableParent.find('tr').each(function(i, tr) {
                var text = $(tr).find('td')
                                .first()
                                .text();
                text = self.normalizeText(text).replace(/[^a-zA-Z]/g, '');
                if (text === attr_name) {
                    result = i;
                    return false;
                }
            });
            return result;
        },

        // If required, this can be used as a general purpose query param getter.
        // The accession number is not necessarily in the URL for GDS.
        // Should we check anyway?
        getDataset: function() {
            var params = window.location.search.substring(1).split('&'),
                i = 0,
                len = params.length;
            for (; i < len; i++)  {
                var keyVal = params[i].split('=');
                if (keyVal[0] == 'acc') {
                    return keyVal[1];
                }
            }
        },

        getOrganism: function() {
            return this.getByName('organism');
        },

        getPlatform: function() {
            return this.getByName('platforms');
        },

        getSamples: function() {
            var A_cols = [],
                B_cols = [];

            $('.g2e-chkbx').each(function(i, input) {
                var $input = $(input),
                    gene;
                if ($input.is(':checked')) {
                    gene = $(input).parent()
                                   .siblings()
                                   .first()
                                   .find('a')
                                   .text();

                    if ($input.hasClass('g2e-control')) {
                        A_cols.push(gene);
                    } else if ($input.hasClass('g2e-experimental')) {
                        B_cols.push(gene);
                    }
                }
            });

            return {
                A_cols: A_cols,
                B_cols: B_cols
            };
        }
    };
};


/* The primary user interface, a single modal box.
 */
function ModalBox(events, tagger, templater, userInputHandler) {

    var $modalBox;
    (function init() {
        var html = templater.get('modal');
        $(html).hide().appendTo('body');
        $('#g2e-modal').draggable();
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
            $('#g2e-' + prop + ' td input').attr('value', html);
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
                    userInputHandler;

                UiEmbedder(events, page, screenScraper, templater);
                userInputHandler = UserInputHandler(comm, events, notifier, screenScraper, tagger);
                ModalBox(events, tagger, templater, userInputHandler);

                events.fire('g2eLoaded');
            }
        });
    }
};

	// The Firefox plugin bootstrapper manages when the plugin loads.
    main();

})(jQuery);
