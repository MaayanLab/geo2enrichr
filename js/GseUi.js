
var GseUi = function(events, templater) {

	var $gse_details;

    var embed = function($hook) {

        $hook.append(templater.get('btn', 'gse'));

        // Find the details table.
        $('table').each(function(i, el) {
            var $el = $(el);
            if ($el.attr('width') === '600' &&
                $el.attr('cellpadding') === '2' &&
                $el.attr('cellspacing') === '0')
            {
                $gse_details = $el;
                return false;
            }
        });

        // Find the samples from the details table.
        $gse_details.find('tr').each(function(i, tr) {
            if ($(tr)
                    .find('td')
                    .first()
                    .text()
                    .toLowerCase()
                    .indexOf('samples') === 0)
            {
                $samples_table = $(tr);
                return false;
            }
        });

        $samples_table
            .find('tr')
            .each(function(i, tr) {
                $(tr).append(templater.get('chkbxs', 'gse'));
            })
            .end()
            .find('table')
            .first()
            .find('tr')
            .first()
            .before(templater.get('thead', 'gse'));

        events.fire('bootstrapped', {
            details: $gse_details,
            table: $samples_table
        });
    };

    var init = function() {
        // Go up two parents to find the table.
        var $hook = $('#geo2r').next();
        if ($hook) {
            embed($hook);
        }
    };

	return {
        init: init
	};
};
