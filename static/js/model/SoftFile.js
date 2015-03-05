App.Model.SoftFile = Backbone.Model.extend({
    urlRoot: '/g2e/getgeo',
    defaults: {
        dataset: '',
        platform: '',
        organism: '',
        A_cols: [],
        B_cols: [],
        cell: '',
        perturbation: '',
        gene: '',
        disease: '',
        diffexpMethod: 'chdir',
        cutoff: 500,
        norm: true
    }
});
