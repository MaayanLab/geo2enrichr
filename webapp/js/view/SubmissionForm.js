var SubmissionForm = Backbone.View.extend({

    el: $('#submissionForm'),

    events: {
        'click #submit-btn': 'submit'
    },

    template: _.template('' +
        '<td id="actions" class="title">' +
            '<button id="submit-btn" class="btn">Extract gene lists</button>' +
        '</td>'
    ),

    initialize: function(options) {
        this.SERVER = options.SERVER;
        this.requiredData = options.requiredData;
        this.metadata = options.metadata;
        this.$el.html(this.template());
    },

    ajax: function(endpoint, type, data, callback) {
        var self = this;
        return $.ajax({
            url: self.SERVER + endpoint,
            type: type,
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            crossDomain: true,
            success: callback
        });
    },

    submit: function(evt) {
        evt.preventDefault();
        var self = this,
            getGeoData = {
                dataset: self.requiredData.get('dataset').get('value'),
                platform: self.requiredData.get('platform').get('value'),
                A_cols: self.requiredData.get('control').get('value').replace(/ /g,'').split(','),
                B_cols: self.requiredData.get('experimental').get('value').replace(/ /g,'').split(',')
            };

        self.ajax('/getgeo', 'PUT', getGeoData, $.noop).then(function(diffExpData) {
            self.ajax('/diffexp', 'POST', diffExpData, function(results) {
                debugger;
            });   
        });
    }
});
