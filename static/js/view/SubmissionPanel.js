App.View.SubmissionPanel = Backbone.View.extend({

    tagName: 'div',

    events: {
        'button': 'submit'
    },

    template: _.template('' +
        '<nav>' +
        '   <button data-command="submit">Submit</button>' +
        '</nav>'
    ),

    events: {
        'click .submit-btn': 'submit'
    },

    template: _.template('<button class="submit-btn" class="btn">Extract gene lists</button>'),

    initialize: function(options) {
        this.parent = options.parent;
        this.$el.append(this.template());
    },

/* Helper fucntions for submitting data.
 * ------------------------------------- */
  
    getData: function() {
        var result = {};

        /* Handles which inputs are used for the current mode; also maps any
         * displayed options to backend options if necessary.
         */
        this.collection.each(function(model) {
            if (model.get(this.parent.mode) >= 0) {
                var key = model.get('id'),
                    val = model.get('value') || model.get('default');
                if (model.get('backend')) {
                    var idx = model.get('options').indexOf(val);
                    result[key] = model.get('backend')[idx];
                } else {
                    result[key] = val;
                }
            }
        }, this);
        
        /* Handles the select samples for GEO mode; the user does not input
         * selected samples on Upload mode.
         */
        if (this.parent.mode === 'geo') {
            var A_cols = this.collection.get('control').get('value'),
                B_cols = this.collection.get('experimental').get('value');
            if (_.isString(A_cols)) {
                A_cols = A_cols.replace(/ /g,'').split(',');
            }
            if (_.isString(B_cols)) {
                B_cols = B_cols.replace(/ /g,'').split(',');
            }
            result.A_cols = A_cols;
            result.B_cols = B_cols;
        }

        return result;
    },

    submit: function() {
        App.EventAggregator.trigger('clear:results');
        if (this.parent.mode === 'geo') {
            this.submitGeoSoftFile();
        } else if (!$(':file').length) {
            this.submitExampleSoftFile();
        } else {
            this.submitCustomSoftFile();
        }
    },

    ajax: function(endpoint, type, data, callback) {
        return $.ajax({
            url: App.SERVER + endpoint,
            type: type,
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            crossDomain: true,
            success: callback
        });
    },
    
    getgeo: function(inputData, results) {
        return this.ajax('/getgeo', 'PUT', inputData, function(responseData) {
            results.soft = {
                link: responseData.link
            }
        });
    },

    diffexp: function(getgeoData, results) {
        return this.ajax('/diffexp', 'POST', getgeoData, function(diffExpData) {
            _.extend(results, diffExpData)
            App.EventAggregator.trigger('downloaded:genes', results);
        });
    },
  
    getcustom: function(formData) {
        return $.ajax({
            url: App.SERVER + '/getcustom',
            type: 'PUT',
            data: formData,
            // Tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    },

    /* Send nothing over the wire, indicating we want the server to parse the
     * example SOFT file.
     */
    getExample: function(results) {
        return this.ajax('/getcustom', 'PUT', {}, function(responseData) {
            results.soft = {
                link: responseData.link
            }
        });
    },

/* Core functions for submitting data.
 * ----------------------------------- */

    submitGeoSoftFile: function() {
        var self = this,
            inputData = this.getData(),
            options = {
                method: inputData.diffexp,
                cutoff: inputData.cutoff
            },
            results = {};
        this.getgeo(inputData, results).then(function(getgeoData) {
            _.extend(getgeoData, options);
            self.diffexp(getgeoData, results).then(function(diffexpData) {
                debugger;  
                self.enrichr(diffexpData);
            });
        });
    },

    submitExampleSoftFile: function() {
        var self = this,
            results = {};
        this.getExample(results).then(function(getgeoData) {
            self.diffexp(getgeoData, results);
        });
    },

    submitCustomSoftFile: function() {
        var self = this,
            results = {},
            formData = new FormData($('form')[0]),
            inputData = this.getData(),
            options = {
                method: inputData.diffexp,
                cutoff: inputData.cutoff
            };

        _.each(inputData, function(v,k) {
            formData.append(k, v);
        });
        this.getcustom(formData).then(function(getcustomData) {
            results.soft = {
                link: getcustomData.link
            }
            _.extend(getcustomData, options);
            self.diffexp(getcustomData, results);
        });
    },

    enrichr: function(options) {
    }
});
