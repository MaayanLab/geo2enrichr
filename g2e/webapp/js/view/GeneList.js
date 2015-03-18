App.View.GeneList = Backbone.View.extend({

    tagName: 'div',

    template: _.template('' +
        '<h3><%= direction %></h3>' +
        '<ul>' +
            '<li><a href="<%= text_file %>" target="_blank">Download gene list</a></li>' +
            '<li><a href="<%= enrichr_link %>">Enrichr</a></li>' +
        '</ul>'
    ),

    initialize: function(options) {
        this.parent = options.parent;
        this.text_file = options.text_file;
        this.enrichr_link = options.enrichr_link;
        //this.model = options.model;
        this.$el.addClass(options.direction);
        this.$el.append(this.template(options));
        this.parent.$el.append(this.$el);
        App.EventAggregator.on('clear:form', this.clear, this);
    },

    clear: function() {
        //d3.select(this.el).selectAll('div').remove();
        //this.hide();
    },

    update: function() {
        /*var data = this.model.get('genes');
        
        if (!data.length) {
            this.clear();
            return;
        }

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
                return genes[i] + '\t' + d;
            });
        this.$el.fadeIn();*/
    }
});
