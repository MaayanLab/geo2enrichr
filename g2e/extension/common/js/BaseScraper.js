
/* BaseScraper contains functions that are used on both GSE and GDS pages.
 * The returned object is then mixed in with a secondary scraper, depending on
 * context.
 */
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
                cutoff = $modal.find('#g2e-cutoff option:selected').val(),
                normalize = $modal.find('#g2e-normalize option:selected').val(),
                cell = $modal.find('#g2e-cell .g2e-value input').val(),
                perturbation = $modal.find('#g2e-perturbation .g2e-value input').val(),
                gene = $modal.find('#g2e-gene #g2e-geneList').val(),
                disease = $modal.find('#g2e-disease #g2e-diseaseList').val(),
                threshold = $modal.find('#g2e-threshold option:selected').val();

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
        },

        /* Gets data from fields that are specific for the upcoming Coursera
         * MOOC. In principle, we can remove this in the future.
         *
         * GWG. August 2015.
         */
        getCrowdsourcingMetadata: function($modal) {
            $('#required-fields-based-on-tag').find('tr').each(function(i, tr) {
                var $tr = $(tr);
                if ($tr.find('input').attr('required') === 'true') {
                    debugger;
                } else {
                    debugger;
                }
            });
            return {};
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
