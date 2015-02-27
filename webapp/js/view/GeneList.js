App.View.GeneList = Backbone.View.extend({

    tagName: 'table',

    events: {
        'click tr td a': 'download'
    },

    template: _.template('' +
        '<h3><%= direction %></h3>' +
        '<a href="<%= App.BASE + "/" + link %>" target="_blank">Download gene list</a>'
    ),

    initialize: function(options) {
        this.model = options.model;
        this.model.on('change', this.update, this);
        App.EventAggregator.on('clear', function() {
            d3.select(this.el).remove();
            this.model.set('genes', []);
            this.hide();
        }, this);
    },

    update: function() {
        var data = this.model.get('genes');
        
        if (!data.length) { return; }

        var unpack = _.unzip(data.slice(0,10)),
            genes = unpack[0],
            values = unpack[1];

        // Recompile the template
        this.$el.html(this.template(this.model.toJSON()));

        var x = d3.scale.linear()
            .domain([0, d3.max(values)])
            .range([0, 420]);

        d3.select(this.el)
            .selectAll('div')
            .data(values)
            .enter()
            .append('div')
            .style("width", function(d) {
                return x(d) + "px";
            })
            .text(function(d, i) {
                return genes[i];
            });

        /*var geneList = this.model.get('genes'),
            html = this.template({
                direction: this.model.get('direction'),
                genes: geneList.slice(0,10)
            });*/
        //this.$el.html(html);
        this.$el.fadeIn();
    }
});
