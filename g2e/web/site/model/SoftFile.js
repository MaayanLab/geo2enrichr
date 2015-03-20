App.Model.SoftFile = Backbone.Model.extend({
    
    urlRoot: '/g2e/getgeo',
    
    sync: function(method, model, options) {
        return Backbone.sync(method, model, options);
    },
    
    defaults: {
        filename: '',
        dataset: '',
        platform: '',
        organism: '',
        A_cols: [],
        B_cols: [],
        file: '',
        cell: '',
        perturbation: '',
        gene: '',
        disease: '',
        diffexpMethod: 'chdir',
        cutoff: 500,
        norm: true
    }
});
