App.View.ResultsPanel = Backbone.View.extend({

    tagName: 'div',

    id: 'results',

    initialize: function(options) {
        debugger;
        this.upModel = new App.Model.GeneList({ direction: 'up' });
        this.downModel = new App.Model.GeneList({ direction: 'down' });
        this.upView = new App.View.GeneList({
            model: this.upModel
        }).hide().appendTo(this);
        this.downView = new App.View.GeneList({
            model: this.downModel
        }).hide().appendTo(this);

        App.EventAggregator.on('downloaded:genes', this.render, this);
        App.EventAggregator.on('clear:form', this.clear, this);
        App.EventAggregator.on('clear:results', this.clear, this);
    },

    render: function(data) {
        this.$el.prepend('<a href="' + App.BASE + '/' + data.soft.link + '">SOFT file</a>');
        this.upModel.set(data.up);
        this.downModel.set(data.down);
    },

    clear: function() {
        this.$el.find('a').remove();
        this.upModel.set({ 'genes': '', 'count': '', 'link': '' });
        this.downModel.set({ 'genes': '', 'count': '', 'link': '' });
    }
});
