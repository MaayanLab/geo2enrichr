App.View.Extraction = Backbone.View.extend({

    tagName: 'div',

    className: 'results content',

    initialize: function(options) {
        this.parent = options.parent;
        this.parent.$el.find('#content').append(this.el);
    },

    render: function(extraction) {
        // In case the user tries to reload the results.
        this.$el.empty();
        this.$el.append('<h2>Results</h2>');

        var sb = new App.View.ShareButton();
        this.$el.append(sb.el);

        var sf = new App.View.SoftFile(extraction.get('softfile'));
        this.$el.append(sf.el);

        var md = new App.View.Metadata(extraction.get('metadata'));
        this.$el.append(md.el);

        var gls = new App.View.GeneLists(extraction.get('genelists'));
        this.$el.append(gls.el);

        this.$el.show();
    },

    error: function(data) {
        this.$el.append('<p class="highlight">Unknown server side error. Please try to refresh the page.</p>');
    }
});
