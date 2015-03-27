var App = {
    Collection: {},
    Model: {},
    View: {},
    EventAggregator: _.extend({}, Backbone.Events)
};

$(function() {

    /* This function handles loading templates from .html files. Notice it
     * needs to be defined *before* the contentViews, which rely upon it.
     */
    var templateCache = {};
    App.renderTemplate = function(name, data) {
        if (!templateCache[name]) {
            var dir = '/g2e/web/site/template/',
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
    var page   = new App.View.Page({
        hash: window.location.hash.slice(1)
    });

    /* contentViews are replaceable views in the SAP; other views are static.
     * The helper functions hide() and show() allow for easy toggling between
     * main views.
     */
    App.contentViews = {
        form: new App.View.Form({
            model: new App.Model.SoftFile(),
            parent: page
        }),
        api: new App.View.Api({
            parent: page
        }),
        tutorial: new App.View.Tutorial({
            parent: page
        }),
        pipeline: new App.View.Pipeline({
            parent: page        
        }),
        about: new App.View.About({
            parent: page
        }),
        extraction: new App.View.Extraction({
            parent: page,
            model: model = new App.Model.Extraction()
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
            'example': 'example',
            'api': 'api',
            'tutorial': 'tutorial',
            'pipeline': 'pipeline',
            'about': 'about',
            'results/(:id)': 'results'
        },
        form: function() {
            App.contentViews.show(App.contentViews.form);
        },
        example: function() {
            App.contentViews.show(App.contentViews.form);
            App.contentViews.form.loadExample();
        },
        api: function() {
            App.contentViews.show(App.contentViews.api);
        },
        tutorial: function() {
            App.contentViews.show(App.contentViews.tutorial);
        },
        pipeline: function() {
            App.contentViews.show(App.contentViews.pipeline);
        },
        about: function() {
            App.contentViews.show(App.contentViews.about);
        },
        results: function(id) {
            var view = App.contentViews.extraction,
                loader = new App.View.LoadingScreen({
                    parent: view
                });
            App.contentViews.show(view);
            view.model.set('id', id);
            model.fetch({
                success: function() {
                    view.render(model);
                },
                error: function(data) {
                    view.error(data);
                },
                complete: function() {
                    loader.stop();
                }
            });
        }
    });

    App.router = new App.Router();

    App.router.bind('all', function(route) {
        if (route === 'route') return;
        page.setNav(route.split(':')[1]);
    });
    
    Backbone.history.start({
        root: '/g2e'
    });
});
