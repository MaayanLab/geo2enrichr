App.View.ResultsPanel = Backbone.View.extend({

    tagName: 'div',

    className: 'geneList',

    initialize: function(options) {
        var upModel = new App.Model.GeneList({ direction: 'up' }),
            downModel = new App.Model.GeneList({ direction: 'down' }),
            upView = new App.View.GeneList({
                model: upModel
            }).hide().appendTo(this),
            downView = new App.View.GeneList({
                model: downModel
            }).hide().appendTo(this);

        App.EventAggregator.on('genesDownloaded', function(data) {
            upModel.set({
                'genes': data.up.genes,
                'count': data.up.count,
                'link': data.up.link
            });
            downModel.set({
                'genes': data.down.genes,
                'count': data.down.count,
                'link': data.down.link
            });
        });
    }
});
