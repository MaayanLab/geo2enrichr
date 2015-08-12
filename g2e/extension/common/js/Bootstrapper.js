
var Bootstrapper = function(events, notifier, templater) {
    
    var isGds = function() {
        var path;
        if (window.location.pathname !== '/') {
            path = window.location.pathname.split('/')[1];
            if (path === 'sites') {
                return 1;
            } else if (path === 'geo') {
                return -1;
            }
            return 0;
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

        var isGdsFl = isGds();
        if (isGdsFl === 1) {
            GdsBootstrapper(events, templater).init();
        } else if (isGdsFl === -1) {
            GseBootstrapper(events, templater).init();
        }
        // Else do nothing.
    };

    return {
        init: init,
        isGds: isGds
    };
};
