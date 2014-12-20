
var GseUi = function(html, events) {

	return {

		embed: function($hook) {
			var self = this;
			$hook.append(html.get('btn', 'gse'));
			$('#g2e-link').click(function() {
				self.openApp();
			});
		},

		init: function() {
			// Go up two parents to find the table.
			var $hook = $('#geo2r').next();
			if ($hook) {
				this.embed($hook);
			}
		}
	};
};
