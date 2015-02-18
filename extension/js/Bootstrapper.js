
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
