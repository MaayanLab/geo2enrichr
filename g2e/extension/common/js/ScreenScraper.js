
/* Contains functions that are used on both GSE and GDS pages. The returned
 * object is a mixin of the general functionality with a context-dependent
 * scraper.
 */
function ScreenScraper(events, page, SUPPORTED_PLATFORMS, onConstructedCallback) {

    var modeScraper,
        $modalButtonParent,
        $metadataTableParent,

        // Globally accessible metadata from API.
        eUtilsApiMetadata = {};

    var scraper = {

        getModalButtonParent: function() {
            return $modalButtonParent;
        },

        getMetadataTableParent: function () {
            return $metadataTableParent;
        },

        isSupportedPlatform: function() {
            // We don't expect the eUtilsApi to return in time. Get the platform by scraping.
            var platform = this._getPlatform();
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
            data.title = eUtilsApiMetadata.title || '';
            data.summary = eUtilsApiMetadata.summary || '';
            data.organism = eUtilsApiMetadata.organism || this._getOrganism();
            data.platform = eUtilsApiMetadata.platform || this._getPlatform();
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

    events.on('eutilsApiFetched', function(data) {
        eUtilsApiMetadata = data;
    });

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