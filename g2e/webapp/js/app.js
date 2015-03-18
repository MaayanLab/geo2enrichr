var App = {
    Collection: {},
    Model: {},
    View: {},
    EventAggregator: _.extend({}, Backbone.Events),
    BASE: 'http://localhost:8083',
    SERVER: 'http://localhost:8083/g2e'
};

$(function() {

    /* This function handles loading templates from .html files. Notice it
     * needs to be defined *before* the contentViews, which rely upon it.
     */
    var templateCache = {};
    App.renderTemplate = function(name, data) {
        if (!templateCache[name]) {
            var dir = '/g2e/template/',
                url = dir + name + '.html',
                string;
            $.ajax({
                url: url,
                dataType: 'html',
                method: 'GET',
                async: false,
                success: function(data) {
                    string = data;
                }
            });
            templateCache[name] = _.template(string);
        }
        return templateCache[name](data);
    };

    /* Bootstraps the page to the DOM, creating the header, nav, and footer.
     */
    var page   = new App.View.Page();

    /* contentViews are replaceable views in the SAP; other views are static.
     * The helper functions hide() and show() allow for easy toggling between
     * main views.
     */
    App.contentViews = {
        form: new App.View.Form({
            model: new App.Model.SoftFile(),
            parent: page
        }),
        help: new App.View.Help({
            parent: page
        }),
        /*news: new App.View.News({
            parent: page
        }),*/
        about: new App.View.About({
            parent: page
        }),
        hide: function() {
            _.each(this, function(view) {
                if (view instanceof Backbone.View) {
                    view.$el.hide();
                }
            });
        },
        show: function(view) {
            this.hide();
            view.$el.show();
        }
    };

    /* Delegates routes, silencing invalid URLs before delegating to the
     * default GEO form view.
     */
    App.Router = Backbone.Router.extend({
        routes: {
            '': 'form',
            'help': 'help',
            'about': 'about',
            'results/(:id)': 'results'
        },
        form: function() {
            App.contentViews.show(App.contentViews.form);
        },
        help: function() {
            App.contentViews.show(App.contentViews.help);
        },
        about: function() {
            App.contentViews.show(App.contentViews.about);
        },
        results: function(id) {
            App.contentViews.hide();
            var extraction = new App.Model.Extraction({ id: id });
            extraction.fetch({
                success: function() {
                    var extractionView = new App.View.Extraction({
                        parent: page,
                        model: extraction
                    });
                    extractionView.render();
                }
            });
        }
    });

    App.router = new App.Router();
    
    Backbone.history.start({
        root: '/g2e'
    });
});
