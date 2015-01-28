
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
