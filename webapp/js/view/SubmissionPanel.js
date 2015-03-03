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

    submit: function() {
        App.EventAggregator.trigger('clear:results');
        if (this.parent.mode === 'geo') {
            this.submitGeoSoftFile();
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

    submitGeoSoftFile: function() {
        var self = this,
            data = this.getData(),
            options = {
                method: data.diffexp,
                cutoff: data.cutoff
            },
            result = {};
        self.ajax('/getgeo', 'PUT', data, $.noop).then(function(getGeoData) {
            result.soft = {
                link: getGeoData.link
            }
            self.ajax('/diffexp', 'POST', _.extend(options, getGeoData), function(diffExpData) {
                App.EventAggregator.trigger('downloaded:genes', _.extend(result, diffExpData));
            });   
        });
    },

    submitCustomSoftFile: function() {
        //var inputString = this.textArea.model.get('value');
        /*this.ajax('/custom', 'POST', inputString, $.noop).then(function(diffExpData) {
            App.EventAggregator.trigger('genesDownloaded', diffExpData);
        });*/

        var formData = new FormData($('form')[0]);
        formData.append('name', this.collection.get('dataset').get('value'));
        formData.append('platform', this.collection.get('platform').get('value'));

        $.ajax({
            url: App.SERVER + '/getcustom',
            type: 'PUT',
            data: formData,
            success: function(data) {
                debugger;
            },
            error: function(data) {
                debugger;
            },
            /*xhr: function() {  // Custom XMLHttpRequest
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){ // Check if upload property exists
                    myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // For handling the progress of the upload
                }
                return myXhr;
            },*/

            // Tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    }
});
