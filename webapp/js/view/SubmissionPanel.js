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

    submitGeoSoftFile: function() {
        var self = this,
            data = {
                dataset: this.collection.get('dataset').get('value'),
                platform: this.collection.get('platform').get('value'),
                A_cols: this.collection.get('control').get('value').replace(/ /g,'').split(','),
                B_cols: this.collection.get('experimental').get('value').replace(/ /g,'').split(',')
            },
            result = {};
        self.ajax('/getgeo', 'PUT', data, $.noop).then(function(getGeoData) {
            result.soft = {
                link: getGeoData.link
            }
            self.ajax('/diffexp', 'POST', getGeoData, function(diffExpData) {
                _.extend(result, diffExpData);
                App.EventAggregator.trigger('downloaded:genes', result);
            });   
        });
    },

    submitCustomSoftFile: function() {
        debugger;
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
