
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
            return $('.acc')[0].id;
        },

        _getOrganism: function() {
            return this.getByName('organism');
        },

        _getPlatform: function() {
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
