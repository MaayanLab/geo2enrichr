
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
