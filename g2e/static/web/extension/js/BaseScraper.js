
var BaseScraper = function(DEBUG) {

    var sData = {};

    return {

        getScrapedData: function($modal) {
            // getSamples() returns an object rather than mutating sData
            // because the function must be mixed in at runtime.
            var samples = this.getSamples();

            sData.A_cols   = samples.A_cols;
            sData.B_cols   = samples.B_cols;
            // Short circuit select saved data; this represents user input.
            sData.dataset  = sData.dataset  || this.getDataset();
            sData.organism = sData.organism || this.getOrganism();
            sData.platform = sData.platform || this.getPlatform();

            return $.extend({}, sData);
        },

        getUserOptions: function($modal) {
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
