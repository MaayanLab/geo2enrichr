
var G2E = (function() {

// This file is built by deploy.sh in the root directory.
var EXTENSION_ID = "jpeoebiembhmjeibpnfdnhbncnbfnhhe";
var DEBUG = true;
var SERVER = "http://localhost:8083/g2e/";

var Comm = function(events, notifier, targetApps, SERVER) {

    var fetchGeneList = (function() {
        $.ajax({
            url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
            type: 'GET',
            dataType: 'JSON',
            success: function(data) {
                events.fire('geneListFetched', data);
            }
        });
    })();

    var postSoftFile = function(input) {
        var $loader = $('<div class="g2e-loader-container"><div class="g2e-loader-modal">Loading...</div></div>');
        $('body').append($loader);
        $.post(SERVER + 'api/extract/geo',
            input,
            function(data) {
                var id = data.extraction_id,
                    url = SERVER + '#results/' + id;
                events.fire('resultsReady', url);
            })
            .fail(function() {
                events.fire('resultsError');
            })
            .always(function() {
                $loader.remove();
            });
    };

    return {
        postSoftFile: postSoftFile
    };
};


var Bootstrapper = function(events, notifier, templater) {
    
    var isGds = function() {
        var path;
        if (window.location.pathname !== '/') {
            path = window.location.pathname.split('/')[1];
            if (path === 'sites') {
                return true;
            } else if (path === 'geo') {
                return false;
            }
        }
    };

    // We may have multiple GEO2[X] extensions installed. Guard against this.
    var extensionAlreadyInstalled = function() {
        if ($('#' + templater.embedBtnId()).length) {
            notifier.log('Another GEO2[X] extension is installed.');
            return true;
        }
        return false;
    };

    var init = function() {
        if (extensionAlreadyInstalled()) {
            return;
        }

        if (isGds()) {
            GdsBootstrapper(events, templater).init();
        } else {
            GseBootstrapper(events, templater).init();
        }
    };

    return {
        init: init,
        isGds: isGds
    };
};


var GdsBootstrapper = function(events, templater) {

    var embed = function($hook) {
        $hook
            .children()
            .last()
            .after(templater.get('btn', 'gds'));
        events.fire('bootstrapped', {
            details: $('#gds_details'),
            hook: $hook
        });
    };

    var init = function() {
        var id = setInterval(function() {
            var $hook = $('#diff_express > tbody');
            if ($hook.length) {
                embed($hook);
                clearInterval(id);
            }
        }, 50);
    };

	return {
        init: init
	};
};


var GseBootstrapper = function(events, templater) {

	var $gse_details;

    var embed = function($hook) {

        $hook.append(templater.get('btn', 'gse'));

        // Find the details table.
        $('table').each(function(i, el) {
            var $el = $(el);
            if ($el.attr('width') === '600' &&
                $el.attr('cellpadding') === '2' &&
                $el.attr('cellspacing') === '0')
            {
                $gse_details = $el;
                return false;
            }
        });

        // Find the samples from the details table.
        $gse_details.find('tr').each(function(i, tr) {
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
                $(tr).append(templater.get('chkbxs', 'gse'));
            })
            .end()
            .find('table')
            .first()
            .find('tr')
            .first()
            .before(templater.get('thead', 'gse'));

        events.fire('bootstrapped', {
            details: $gse_details,
            table: $samples_table
        });
    };

    var init = function() {
        // Go up two parents to find the table.
        var $hook = $('#geo2r').next();
        embed($hook);
    };

	return {
        init: init
	};
};


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


var TargetApps = function(events) {

    /* Set default. */
    var currentApp = 'enrichr';

    var $resultsTitle, $resultsValue;

    setTimeout(function() {
        $resultsTitle = $('#g2e-results-title');
        $resultsValue = $('#g2e-results-value');
    }, 1000);

    var apps = {
        enrichr: {
            name: 'Enrichr',
            selectValue: 'enrichr',
            color: '#d90000',
            endpoint: 'enrichr',
            resultsFormatter: function(geneLists) {
                $resultsTitle.html('<strong>Enriched genes:</strong>');
                if (geneLists.up === '' ||
                    geneLists.down === '' ||
                    geneLists.combined === '') {
                    $resultsValue.html('' +
                        '<span class="g2e-error">Timeout using Enrichr. Please try again later.</span>'
                    );
                } else {
                    $resultsValue.html('' +
                        '<button id="g2e-enrichr-up">Up</button>' +
                        '<button id="g2e-enrichr-down">Down</button>' +
                        '<button id="g2e-enrichr-combined">All</button>');

                    $('#g2e-enrichr-up').click(function() {
                        window.open(geneLists.up, '_blank');
                    });
                    
                    $('#g2e-enrichr-down').click(function() {
                        window.open(geneLists.down, '_blank');
                    });

                    $('#g2e-enrichr-combined').click(function() {
                        window.open(geneLists.combined, '_blank');
                    });
                }
            }
        },  
        l1000cds: {
            name: 'L1000CDS',
            selectValue: 'l1000cds',
            color: '#6CAB6D',
            endpoint: 'stringify',
            resultsFormatter: function(geneLists) {
                $resultsTitle.html('<strong>Perturbagens:</strong>');
                $resultsValue.html('<button id="g2e-l1000">Go to L1000CDS</button>');

                $('#g2e-l1000').click(function(data) {
                    var $form = $('form'),
                        params = {
                            upGenes: JSON.stringify(geneLists.up.split('-')),
                            dnGenes: JSON.stringify(geneLists.down.split('-'))
                        };

                    $form.attr({
                        'action': 'http://amp.pharm.mssm.edu/L1000CDS/input',
                        'method': 'POST'
                    });

                    $.each(params, function(name, val) {
                        $form.append(
                            $('input').attr({
                                'type': 'hidden',
                                'name': name,
                                'value': val
                            })
                        );
                    });

                    $('body').append($form);
                    $form.submit();
                });
            },
        }
    };

    return {
        set: function(newApp) {
            currentApp = newApp;
        },
        current: function() {
            return apps[currentApp];
        },
        all: function() {
            return apps;
        }
    };
};

/*$('#g2e-l1000').click(function(data) {
    var //$form = $('form'),
        method = 'post',
        path = 'http://amp.pharm.mssm.edu/L1000CDS/input',
        params = {
            upGenes: JSON.stringify(geneLists.up.split('-')),
            dnGenes: JSON.stringify(geneLists.down.split('-'))
        };

    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
});*/


var Templater = function(EXTENSION_ID, targetApps) {

    var LOGO50X50 = 'chrome-extension://' + EXTENSION_ID + '/image/logo-50x50.png';

    var targetAppsOptions = function() {
        var options = '';
        $.each(targetApps.all(), function(i, app) {
            options += '<option value="' + app.selectValue + '"';
            if (app == targetApps.current()) {
                 options += 'selected="selected"';
            }
            options += '>' + app.name;
            options += '</option>';
        });
        return options;
    };

    var modal = '' +
        '<div id="g2e-overlay">' +
            '<div id="g2e-modal">' +
                '<div id="g2e-title">' +
                    '<a href="http://maayanlab.net/g2e/" target="_blank">' +
                        '<img src="' + LOGO50X50 + '">' +
                        '<span>GEO2</span>' +
                        '<span id="g2e-target-app-title" style="color:' + targetApps.current().color + ';">' +
                            targetApps.current().name +
                        '</span>' +
                    '</a>' +
                '</div>' +
                '<div id="g2e-nav">' +
                    '<button id="g2e-close-btn" class="g2e-btn">&#10006</button>' +
                '</div>' +
                '<div class="g2e-clear"></div>' +
                '<table id="g2e-main-tbl">' +
                    '<tr>' +
                        '<td id="g2e-confirm">' +
                            '<div class="g2e-lowlight g2e-bottom">Please verify that your data is correct, *required.</div>' +
                            '<table class="g2e-confirm-tbl">' +
                                '<tr id="g2e-diffexp">' +
                                    '<td class="g2e-title">' +
                                        '<label>Differential expression method</label>' +
                                    '</td>' +
                                    '<td class="g2e-value">' +
                                        '<select>' +
                                            '<option value="chdir">Characteristic direction</option>' +
                                            '<option value="ttest">T-test</option>' +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-dataset">' +
                                    '<td class="g2e-title">Accession num.&#42;</td>' +
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
                                    '<td class="g2e-title">Control samples&#42;</td>' +
                                    '<td class="g2e-value"></td>' +
                                '</tr>' +
                                '<tr id="g2e-B_cols" class="g2e-last">' +
                                    '<td class="g2e-title">Treatment or condition samples&#42;</td>' +
                                    '<td class="g2e-value"></td>' +
                                '</tr>' +
                            '</table>' +
                            '<div class="g2e-lowlight g2e-bottom">Please fill out these optional annotations, **if relevant.</div>' +
                            '<table class="g2e-confirm-tbl">' +
                                '<tr id="g2e-cell">' +
                                    '<td class="g2e-title">' +
                                        '<label>Cell type or tissue</label>' +
                                    '</td>' +
                                    '<td class="g2e-value">' +
                                        '<input placeholder="No data">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-perturbation">' +
                                    '<td class="g2e-title">' +
                                        '<label>Perturbation</label>' +
                                    '</td>' +
                                    '<td class="g2e-value">' +
                                        '<input placeholder="No data">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-gene" class="ui-widget">' +
                                    '<td class="g2e-title">' +
                                        '<label for="g2e-geneList">Manipulated gene**</label>' +
                                    '</td>' +
                                    '<td class="g2e-value">' +
                                        '<input id="g2e-geneList" placeholder="No data">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr id="g2e-disease" class="ui-widget g2e-last">' +
                                    '<td class="g2e-title">' +
                                        '<label for="g2e-diseaseList">Rare disease**</label>' +
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
                        'GEO2Enrichr is being developed by the <a href="http://icahn.mssm.edu/research/labs/maayan-laboratory" target="_blank">Ma\'ayan Lab</a>.' +
                        ' See the <a href="http://maayanlab.net/g2e/" target="_blank">documentation</a> for details.' +
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
                        '<img src="' + LOGO50X50 + '">' +
                    '</td>' +
                '</tr>')
        },
        'gse': {
            'btn': $('' +
                '<tr>' +
                    '<td id="' + EMBED_BTN_ID + '">' +
                        '<span id="g2e-link">' + BUTTON_TEXT + '</span>' +
                        '<img src="' + LOGO50X50 + '">' +
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


var Notifier = function(DEBUG) {

	var log = function(msg) {
		if (DEBUG) {
			console.log(msg);
		}
	};

	var ask = function(msg, deflt) {
		return prompt(msg, deflt);
	};

	var warn = function(msg) {
		alert(msg);
	};

	return {
		log: log,
		ask: ask,
		warn: warn
	};
};


var BaseScraper = function(DEBUG) {

    return {

        getScrapedData: function($modal) {
            var data = {},
                samples = this.getSamples();

            data.A_cols   = samples.A_cols;
            data.B_cols   = samples.B_cols;
            // Short circuit select saved data; this represents user input.
            data.dataset  = this.getDataset();
            data.organism = this.getOrganism();
            data.platform = this.getPlatform();

            return data;
        },

        getUserOptions: function($modal) {
            var data = {},
                method = $modal.find('#g2e-diffexp option:selected').val(),
                cell = $modal.find('#g2e-cell .g2e-value input').val(),
                perturbation = $modal.find('#g2e-perturbation .g2e-value input').val(),
                gene = $modal.find('#g2e-gene #g2e-geneList').val();
                disease = $modal.find('#g2e-disease #g2e-diseaseList').val();
            
            if (method) {
                data.method = method;
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
};


var GdsScraper = function(events) {

    var $details,
        $hook;

    events.on('bootstrapped', function(data) {
        $details = data.details;
        $hook = data.hook;
    });

    return {

        getDataset: function() {
            var record_caption = $details.find('.caption').text(),
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
            var $groupRow = $($hook.children().find('tbody td')[0]),
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
            var text = $($details.find('tr')[idx]).text();
            // Remove any preceding whitespace.
            return text.split(':')[1].replace(/\s*/, '');
        },

        getRowIdxFromName: function(attrName) {
            var self = this,
                result;
            $details.find('tr').each(function(i, tr) {
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


var GseScraper = function(events) {

    var $details;

    events.on('bootstrapped', function(data) {
        $details = data.details;
    });

    return {

        getByName: function(name) {
            var idx = this.getRowIdxByName(name);
            return $($details.find('tr')[idx]).find('a').text();
        },

        getRowIdxByName: function(attr_name) {
            var self = this,
                result;
            $details.find('tr').each(function(i, tr) {
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


var Ui = function(comm, events, notifier, scraper, SUPPORTED_PLATFORMS, targetApps, templater) {

    var geneList, $overlay, $resultsBtn, $submitBtn, $errorMessage;

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

    var resetFooter = function() {
        $resultsBtn.hide().off();
        $submitBtn.removeClass('g2e-lock').off().click(postData);
        $errorMessage.hide();
    };

    var postData = function() {
        var scrapedData = scraper.getScrapedData($overlay),
            userOptions = scraper.getUserOptions($overlay),
            allData = $.extend({}, scrapedData, userOptions);
        if (isValidData(scrapedData)) {
            $(this).addClass('g2e-lock').off();
            comm.postSoftFile(allData);
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

    events.on('resultsError', function() {
        $errorMessage.show();
    });

    var init = (function() {
        var html = templater.get('modal');
        $(html).hide().appendTo('body');
        $('#g2e-modal').draggable();
        $overlay = $('#g2e-overlay');
        $resultsBtn = $overlay.find('#g2e-results-btn');
        $errorMessage = $overlay.find('#g2e-error-message').hide();
        $submitBtn = $overlay.find('#g2e-submit-btn').click(postData);
        $overlay.find('#g2e-close-btn').click(function() {
            resetFooter();
            $overlay.hide();
        });
    })();
};

var main = function() {

    var SUPPORTED_PLATFORMS = ['GPL8321', 'GPL7091', 'GPL3307', 'GPL8300', 'GPL11383', 'GPL13158', 'GPL4044', 'GPL1426', 'GPL6887', 'GPL3084', 'GPL32', 'GPL16268', 'GPL13692', 'GPL2881', 'GPL15207', 'GPL3697', 'GPL91', 'GPL339', 'GPL96', 'GPL17518', 'GPL15401', 'GPL13712', 'GPL201', 'GPL1261', 'GPL10558', 'GPL6193', 'GPL6244', 'GPL3050', 'GPL6101', 'GPL6885', 'GPL4685', 'GPL6102', 'GPL4200', 'GPL6480', 'GPL6106', 'GPL6845', 'GPL7202', 'GPL4134', 'GPL1708', 'GPL3921', 'GPL85', 'GPL4074', 'GPL2897', 'GPL4133', 'GPL6947', 'GPL1536', 'GPL1355', 'GPL4487', 'GPL81', 'GPL6096', 'GPL8063', 'GPL11202', 'GPL16686', 'GPL15792', 'GPL6246', 'GPL340', 'GPL11180', 'GPL13497', 'GPL571', 'GPL570'];
    
    /* EXTENSION_ID, DEBUG, SERVER, and SUPPORTED_PLATFORMS are set in
     * config.js via deploy.sh.
     */
    var events = Events(),
        notifier = Notifier(DEBUG),
        targetApps = TargetApps(events),
        templater = Templater(EXTENSION_ID, targetApps),
        baseScraper = BaseScraper(DEBUG),
        bootstrapper = Bootstrapper(events, notifier, templater),
        scraper,
        ui,
        comm;

    if (bootstrapper.isGds()) {
        modeScraper = GdsScraper(events);
    } else {
        modeScraper = GseScraper(events, templater);
    }

    scraper = $.extend(modeScraper, baseScraper);
    comm = Comm(events, notifier, targetApps, SERVER);
    ui = Ui(comm, events, notifier, scraper, SUPPORTED_PLATFORMS, targetApps, templater);
    
    bootstrapper.init();
    notifier.log('g2e loaded.');
};


	window.onload = main();

})(jQuery);
