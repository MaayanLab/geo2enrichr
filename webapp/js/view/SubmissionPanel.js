App.View.SubmissionPanel = Backbone.View.extend({

    tagName: 'div',

    events: {
        'click .submit-btn': 'submit'
    },

    template: _.template('<button class="submit-btn" class="btn">Extract gene lists</button>'),

    initialize: function(options) {
        this.parent = options.parent;
    },

    submit: function() {
        if (this.parent.mode === 'geo') {
            this.submitGeoSoftFile();
        } else {
            this.submitCustomSoftFile();
        }
    },

    ajax: function(endpoint, type, data, callback) {
        var self = this;
        return $.ajax({
            url: App.SERVER + endpoint,
            type: type,
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            crossDomain: true,
            success: callback
        });
    },

    submitGeoSoftFile: function() {
        var self = this,
            data = {
                dataset: this.collection.get('dataset').get('value'),
                platform: this.collection.get('platform').get('value'),
                A_cols: this.collection.get('control').get('value').replace(/ /g,'').split(','),
                B_cols: this.collection.get('experimental').get('value').replace(/ /g,'').split(',')
            };
        self.ajax('/getgeo', 'PUT', data, $.noop).then(function(getGeoData) {
            self.ajax('/diffexp', 'POST', getGeoData, function(diffExpData) {
                App.EventAggregator.trigger('genesDownloaded', diffExpData);
            });   
        });
    },

    submitCustomSoftFile: function() {
        var self = this,
            data = {
                dataset: this.collection.get('dataset').get('value'),
                platform: this.collection.get('platform').get('value'),
                A_cols: this.collection.get('control').get('value').replace(/ /g,'').split(','),
                B_cols: this.collection.get('experimental').get('value').replace(/ /g,'').split(',')
            };
        self.ajax('/custom', 'POST', data, $.noop).then(function(diffExpData) {
            App.EventAggregator.trigger('genesDownloaded', diffExpData);
        });
    }
});
