$(function() {

    (function setupSearch() {

        var API_URL = 'api/suggest/',
            $input = $('.search-bar').find('input');

        $.ajax({
			method: 'GET',
			url: API_URL,
			success: function() {
				var tokens = new Bloodhound({
					datumTokenizer: function(datum) {
						return Bloodhound.tokenizers.whitespace(datum.value);
				    },
					queryTokenizer: Bloodhound.tokenizers.whitespace,
					remote: {
						url: API_URL + '%QUERY',
						wildcard: '%QUERY'
					}
				});
				$input
					.typeahead({
						hint: true,
						highlight: true,
						minLength: 1
					},
					{
						name: 'suggestions',
						source: tokens.ttAdapter()
					});
			}
		});
    })();
});