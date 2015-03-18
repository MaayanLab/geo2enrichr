App.View.Extraction = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    initialize: function(options) {
        this.parent = options.parent;
        this.parent.$el.find('#content').append(this.el);
        this.$loader = $('<div class="loader"><pre class="modal">Loading   </pre></div>').hide();
        $('body').append(this.$loader);
    },

    render: function(extraction) {
        _.each(extraction.get('genelists'), function(gl) {
            var gl = new App.View.GeneList({
                text_file: gl.text_file,
                enrichr_link: gl.enrichr_link,
                direction: gl.direction
            });
            this.$el.append(gl.el);
        }, this);
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
