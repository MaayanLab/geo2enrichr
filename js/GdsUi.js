
var GdsUi = function(templater, events) {

	return {

		embed: function($hook) {
			var self = this;
			$hook.children().last().after(templater.get('btn', 'gds'));

			events.fire('uiReady', {
				details: $('#gds_details')
			});

			$('#g2e-link').click(function() {
				self.openModalBox();
			});
		},

		init: function() {
			var self = this,
				id;
			id = setInterval(function() {
				var $hook = $('#diff_express > tbody');
				if ($hook.length) {
					events.fire('embedded', $hook);
					self.embed($hook);
					clearInterval(id);
				}
			}, 250);
		}
	};
};
