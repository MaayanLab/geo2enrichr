App.View.SubmissionPanel = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    template: _.template('' +
        '<td id="actions" class="title">' +
            '<button class="submit-btn" class="btn">Extract gene lists</button>' +
        '</td>'
    ),

    initialize: function(options) {
        this.SERVER = options.SERVER;
        this.upGenes = new App.Model.GeneList();
        this.downGenes = new App.Model.GeneList();
        this.render();
    },

    render: function() {
        this.upGenesResult = new App.View.ResultList({
            model: this.upGenes
        });
        this.downGenesResult = new App.View.ResultList({
            model: this.upGenes
        });
        this.$el.html(this.template());
        this.$el.append(this.upGenesResult.$el);
        this.$el.append(this.downGenesResult.$el);
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

    submit: function(data) {
        var self = this;
        self.ajax('/getgeo', 'PUT', data, $.noop).then(function(getGeoData) {
            self.ajax('/diffexp', 'POST', getGeoData, function(diffExpData) {
                self.upGenes.set('genes', diffExpData.up.genes);
                self.downGenes.set('genes', diffExpData.down.genes);
            });   
        });
    },

    submitCustomSoftFile: function(data) {
        var self = this;
        self.ajax('/custom', 'POST', data, $.noop).then(function(customData) {
            self.upGenes.set('genes', customData.up.genes);
            self.downGenes.set('genes', customData.down.genes);
        });
    }
});
