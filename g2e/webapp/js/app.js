var App = {
    Collection: {},
    Model: {},
    View: {},
    EventAggregator: _.extend({}, Backbone.Events),
    BASE: 'http://localhost:8083',
    SERVER: 'http://localhost:8083/g2e'
};

$(function() {

    /* Bootstraps the page to the DOM, creating the header, nav, and footer.
     */
    var page = new App.View.Page();

    /* contentViews are replaceable views in the SAP; other views are static.
     * The helper function below allows for easy toggling between main views.
     */
    App.contentViews = {
        index: new App.View.Index({
            parent: page
        }),
        about: new App.View.About({
            parent: page
        }),
        documentation: new App.View.Documentation({
            parent: page
        })
    };

    App.show = function(view) {
        _.each(App.contentViews, function(v) {
            v.$el.hide();
        });
        view.$el.show();
    };

    /* Delegates routes, silencing invalid URLs before delegating to the
     * default GEO form view.
     */
    App.Router = Backbone.Router.extend({
        routes: {
            '(soft)': 'index',
            'results/(:id)': 'results',
            'soft/:mode(/:qs)': 'soft',
            'upload(?*queryString)': 'upload',
            'documentation': 'documentation',
            'about': 'about'
        },
        index: function(qs) {
            qs = _.isNull(qs) ? {} : App.objectFromQs(qs);
            App.contentViews.index.rerender('geo', qs);
            App.show(App.contentViews.index);
        },
        results: function(id) {
            var results = new App.Model.Results({ id: id });
            results.fetch({
                success: function() {
                    var resultsView = new App.View.Results({
                        parent: page,
                        model: results
                    });
                    resultsView.render();
                }
            });
        },
        soft: function(mode, qs) {
            qs = App.objectFromQs(qs);
            App.contentViews.index.rerender(mode, qs);
            App.show(App.contentViews.index);
        },
        documentation: function() {
            App.show(App.contentViews.documentation);
        },
        about: function() {
            App.show(App.contentViews.about);
        }
    });

    App.router = new App.Router();
    
    App.objectFromQs = function(queryString) {
        if (_.isNull(queryString) || _.isUndefined(queryString))
            return '';
        var result = {},
            queryString = queryString.split('&');
        _.each(queryString, function(frag) {
            var key, value;
            f = frag.split('=');
            key = f[0];
            value = f[1];
            if (value.indexOf(',') > 0) {
                value = value.split(',');
            } else if (value.indexOf('+') > 0) {
                value = value.replace('+', ' ');
            }
            result[key] = value;
        });
        return result;
    };

    Backbone.history.start({
        root: '/g2e'
    });
});
