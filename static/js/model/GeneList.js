App.Model.GeneList = Backbone.Model.extend({
    urlRoot: '/g2e/diffexp',
    defaults: {
        A: [],
        B: [],
        genes: [],
        direction: '',
        genes: [],
        count: 0,
        link: ''
    }
});
