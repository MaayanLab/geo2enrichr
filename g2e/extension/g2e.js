
var G2E = (function() {

var SUPPORTED_PLATFORMS = ['GPL8321', 'GPL7091', 'GPL3307', 'GPL8300', 'GPL11383', 'GPL13158', 'GPL4044', 'GPL1426', 'GPL6887', 'GPL3084', 'GPL32', 'GPL16268', 'GPL13692', 'GPL2881', 'GPL15207', 'GPL3697', 'GPL91', 'GPL339', 'GPL96', 'GPL17518', 'GPL15401', 'GPL13712', 'GPL201', 'GPL1261', 'GPL10558', 'GPL6193', 'GPL6244', 'GPL3050', 'GPL6101', 'GPL6885', 'GPL4685', 'GPL6102', 'GPL4200', 'GPL6480', 'GPL6106', 'GPL6845', 'GPL7202', 'GPL4134', 'GPL1708', 'GPL3921', 'GPL85', 'GPL4074', 'GPL2897', 'GPL4133', 'GPL6947', 'GPL1536', 'GPL1355', 'GPL4487', 'GPL81', 'GPL6096', 'GPL8063', 'GPL11202', 'GPL16686', 'GPL15792', 'GPL6246', 'GPL340', 'GPL11180', 'GPL13497', 'GPL571', 'GPL570'];
// This file is built by deploy.sh in the root directory.
var EXTENSION_ID = "ggnfmgkbdnedgillmfoakkajnpeakbel";
var DEBUG = true;
var SERVER = "http://localhost:8083/g2e/";

var Comm = function(events, notifier, targetApps, SERVER) {

	var fetchGeneList = function() {
		$.ajax({
			url: 'http://amp.pharm.mssm.edu/Enrichr/json/genemap.json',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('geneListFetched', data);
			}
		});
	}();

	var fetchRareDiseases = function() {
 		$.ajax({
			url: SERVER + 'diseases',
			type: 'GET',
			dataType: 'JSON',
			success: function(data) {
				events.fire('rareDiseasesFetched', data.rare_diseases);
			}
		});       
	}();

	/* This is the workhorse function that chains together multiple AJX
	 * requests to the back-end.
	 */
	var downloadDiffExp = function(input) {
  
        var getAjax = function(endpoint, type, data, callback) {
            return $.ajax({
                url: SERVER + endpoint,
                type: type,
                data: JSON.stringify(data),
                contentType: 'application/json;charset=UTF-8',
                crossDomain: true,
                success: callback
            });
        };

        var isError = function(data) {
            return data.status === 'error';
        };

        var errorHandler = function(data) {
            events.fire('requestFailed', data);
        };

		function dlgeo() {
			var data = {
                accession: input.accession,
                organism: input.organism,
                platform: input.platform,
                method: input.method,
                cell: input.cell,
                perturbation: input.perturbation,
                gene: input.gene,
                disease: input.disease
            };

			var success = function(data) {
                if (isError(data)) {
                    errorHandler(data);
                    return;
                }
                notifier.log('GEO files were downloaded');
                notifier.log(data);
                events.fire('progressBar');
            };

			return getAjax('dlgeo', 'PUT', data, success);
		}

		function diffexp(dlgeoData) {
			var data = {
                // This is the SOFT file, not the gene file.
                accession: input.accession,
                filename: dlgeoData.filename,
                platform: input.platform,
                organism: input.organism,
                control: input.control.join('-'),
                experimental: input.experimental.join('-'),
                cell: input.cell,
                perturbation: input.perturbation,
                gene: input.gene,
                disease: input.disease,
                method: input.method
            };

			var success = function(data) {
                if (isError(data)) {
                    errorHandler(data);
                    return;
                }
                var DIR = 'static/genes/';
                notifier.log('GEO files were differentially expressed');
                notifier.log(data);
                events.fire('progressBar');
                events.fire('dataDiffExped', {
                    'up': SERVER + DIR + data.up,
                    'down': SERVER + DIR + data.down
                });
            };

			return getAjax('diffexp', 'POST', data, success);
		}

		function pipe(diffExpData) {
            var data = {
                'up': diffExpData.up,
                'down': diffExpData.down,
                'combined': diffExpData.combined
            };

            var success = function(data) {
                if (isError(data)) {
                    errorHandler(data);
                    return;
                }
                notifier.log('Enrichr link was returned');
                notifier.log(data);
                events.fire('progressBar');
                events.fire('genesEnriched', data);
            };

            return getAjax(targetApps.current().endpoint, 'POST', data, success);
        }

		/* Pass in noops so that we do nothing if the promise is not returned.
		 */
		dlgeo().then(diffexp, $.noop).then(pipe, $.noop);
	};

	return {
		downloadDiffExp: downloadDiffExp
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


var G2EComm = function(events, notifier, SERVER, TARGET_APP_ENDPOINT) {

};


var LssrComm = function(comm, events, notifier, SERVER, TARGET_APP_ENDPOINT) {

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

	var LOGO50X50 = 'chrome-extension://' + EXTENSION_ID + '/images/g2e-logo-50x50.png';

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

	var $modal = $('' +
		'<div id="g2e-container">' +
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
						    /*'<div class="g2e-lowlight">Please confirm the target application.</div>' +
                            '<table class="g2e-confirm-tbl">' +
                                '<tr id="g2e-target-app-select">' +
                                    '<td class="g2e-title">' +
                                        '<label>Target application</label>' +
                                    '</td>' +
                                    '<td>' +
                                        '<select>' +
                                            targetAppsOptions() +
                                        '</select>' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +*/
							'<div class="g2e-lowlight g2e-bottom">Please verify that your data is correct, *required.</div>' +
							'<table class="g2e-confirm-tbl">' +
								'<tr id="g2e-diffexp">' +
									'<td class="g2e-title">' +
										'<label>Differential expression method</label>' +
									'</td>' +
									'<td class="g2e-value">' +
										'<select>' +
											'<option>Characteristic direction</option>' +
											'<option>T-test</option>' +
										'</select>' +
									'</td>' +
								'</tr>' +
								'<tr id="g2e-accession">' +
									'<td class="g2e-title">Accession num.&#42;</td>' +
									'<td class="g2e-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-platform">' +
									'<td class="g2e-title">Platform</td>' +
									'<td class="g2e-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-organism">' +
									'<td class="g2e-title">Organism</td>' +
									'<td class="g2e-value g2e-editable"></td>' +
								'</tr>' +
								'<tr id="g2e-control">' +
									'<td class="g2e-title">Control samples&#42;</td>' +
									'<td class="g2e-value"></td>' +
								'</tr>' +
								'<tr id="g2e-experimental" class="g2e-last">' +
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
				'<div id="g2e-footer">' +
					'<table>' +
						'<tr>' +
							'<td id="g2e-actions" class="g2e-title">' +
								'<button id="g2e-submit-btn" class="g2e-btn">Extract gene lists</button>' +
							'</td>' +
							'<td id="g2e-progress-bar">' +
								'<div id="g2e-step1" class="g2e-progress">Downloading GEO files</div>' +
								'<div id="g2e-step2" class="g2e-progress">Cleaning data and identifying differential expression</div>' +
								'<div id="g2e-step3" class="g2e-progress">Enriching gene lists</div>' +
								'<div id="g2e-step4" class="g2e-progress">Done!</div>' +
							'</td>' +
						'</tr>' +
					'</table>' +
				    '<table id="g2e-results">' +
                        '<tr id="g2e-downloads">' +
                            '<td class="g2e-title">' +
                                '<strong>Downloads:</strong>' +
                            '</td>' +
                            '<td>' +
                                '<button id="g2e-download-btn" class="g2e-btn">Download gene list</button>' +
                            '</td>' +
                        '</tr>' +

                        // This is filled in by the TargetApps module.
                        '<td id="g2e-results-title" class="g2e-title"></td>' +
                        '<td id="g2e-results-value" class="g2e-value"></td>' +
                    '</table>' +
                    '<p id="g2e-credits">' + 
                        'GEO2Enrichr is being developed by the <a href="http://icahn.mssm.edu/research/labs/maayan-laboratory" target="_blank">Ma\'ayan Lab</a>.' +
                        ' See the <a href="http://maayanlab.net/g2e/" target="_blank">documentation</a> for details.' +
                    '</p>' +
                '</div>' +
			'</div>' +
		'</div>');

    var BUTTON_TEXT = 'Extract knowledge with <strong class="g2e-strong">GEO2Enrichr</strong>';

    var EMBED_BTN_ID ="g2e-embedded-button";

	var templates = {
		'modal': $modal,
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

	var sData = {};

    return {

		getData: function($modal) {
			// getSamples() returns an object rather than mutating sData
			// because the function must be mixed in at runtime.
			var samples = this.getSamples();
			if ($modal) {
				this.getOptions($modal);
			}

			sData.control      = samples.control;
			sData.experimental = samples.experimental;
			// Short circuit select saved data; this represents user input.
			sData.accession    = sData.accession || this.getAccession();
			sData.organism     = sData.organism || this.getOrganism();
			sData.platform     = sData.platform || this.getPlatform();

			return $.extend({}, sData);
		},

		setData: function(key, val) {
			if (key == 'cell' || key == 'platform') {
				val = val.replace(/_|-|\./g, '');
			}
			sData[key] = val;
		},

		getOptions: function($modal) {
			var method = $modal.find('#g2e-diffexp option:selected').val(),
				cell = $modal.find('#g2e-cell td.g2e-value input').val(),
				perturbation = $modal.find('#g2e-perturbation td.g2e-value input').val(),
			    gene = $modal.find('#g2e-gene #g2e-geneList').val();
			    disease = $modal.find('#g2e-disease #g2e-diseaseList').val();
            
			if (method) {
				sData.method = method;
			}
			if (cell) {
				sData.cell = cell.replace(/_|\.|-/, '');
			}
			if (perturbation) {
				sData.perturbation = perturbation.replace(/_|\.|-/, '');	
			}
			if (gene) {
				sData.gene = gene;
			}
			if (disease) {
                sData.disease = disease;
			}
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

		getAccession: function() {
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
				samplesBkpIdx, control, experimental;

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
				control: samplesArr.slice(0, samplesBkpIdx),
				experimental: samplesArr.slice(samplesBkpIdx, samplesArr.length)
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
		getAccession: function() {
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
			var control = [],
				experimental = [];

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
						control.push(gene);
					} else if ($input.hasClass('g2e-experimental')) {
						experimental.push(gene);
					}
				}
			});

			return {
				control: control,
				experimental: experimental
			};
		}
	};
};


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
			key: 'control',
			formatter: function(data) {
				return data.join(', ');
			}
		},
		'g2e-experimental': {
			key: 'experimental',
			formatter: function(data) {
				return data.join(', ');
			}
		}
	};
	
	var steps = ['#g2e-step1', '#g2e-step2', '#g2e-step3', '#g2e-step4'];

	var geneList, $overlay, $modal, $progress, $results;

	// This is called once at startup. All variables and bindings should be permanent.
	var init = function() {
		$modal = templater.get('modal');
		$overlay = $modal.hide().appendTo('body');
		$('#g2e-container #g2e-modal').draggable();
		$progress = $progress || $('#g2e-progress-bar');
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

	var highlightNextStep = function() {
		$progress.find(steps.shift()).addClass('g2e-ready');
	};

	var setDownloadLinks = function(downloadLinks) {
		$results.find('#g2e-download-btn')
				.click(function() {
					downloadUrl(downloadLinks.up);
					setTimeout(function() {
						downloadUrl(downloadLinks.down);
					}, 1000);
				})
				.end();
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
		// Reset progress bar.
		steps = ['#g2e-step1', '#g2e-step2', '#g2e-step3', '#g2e-step4'];
		$progress.hide()
				 .find('.g2e-progress')
				 .removeClass('g2e-ready');

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
					  $progress.show();
					  highlightNextStep();
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
		if (!data.control || data.control.length < 2) {
			notifier.warn('Please select 2 or more control samples');
			return false;
		}
		if (!data.experimental || data.experimental.length < 2) {
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

	events.on('progressBar', highlightNextStep);

	events.on('dataDiffExped', setDownloadLinks);

	events.on('genesEnriched', showResults);
	
	init();

	return {
		openModalBox: openModalBox
	};
};

var main = function() {

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
