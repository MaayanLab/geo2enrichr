App.View.Extraction = Backbone.View.extend({

    tagName: 'div',

    className: 'results content',

    initialize: function(options) {
        this.parent = options.parent;
        this.parent.$el.find('#content').append(this.el);
        this.$loader = $('<div class="loader"><pre class="modal">Loading   </pre></div>').hide();
        $('body').append(this.$loader);
    },

    render: function(extraction) {
        // In case the user tries to reload the results.
        this.$el.empty();

        var sf = new App.View.SoftFile(extraction.get('softfile'));
        this.$el.append(sf.el);

        var md = new App.View.Metadata(extraction.get('metadata'));
        this.$el.append(md.el);

        var gls = new App.View.GeneLists(extraction.get('genelists'));
        this.$el.append(gls.el);

        this.$el.show();
    },

    startLoad: function() {
        var $modal = this.$loader.find('.modal'),
            i = 0,
            MAX = 4;
        this.$loader.fadeIn();
        this.loadingId = setInterval(function() {
            i = ++i % MAX;
            $modal.html('Loading' + Array(i+1).join('.') + Array(MAX-i).join(' '));
        }, 400);
    },

    stopLoad: function() {
        clearInterval(this.loadingId);
        this.$loader.fadeOut();
    }
});
