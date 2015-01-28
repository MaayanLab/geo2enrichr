
var GdsUi = function(events, templater) {

    var embed = function($hook) {
        $hook.children().last().after(templater.get('btn', 'gds'));
        events.fire('bootstrapped', {
            details: $('#gds_details'),
            hook: $hook
        });
    };

    var init = function() {
        var id = setInterval(function() {
            var $hook = $('#diff_express > tbody');
            if ($hook.length) {
                embed($hook);
                clearInterval(id);
            }
        }, 50);
    };

	return {
        init: init
	};
};
