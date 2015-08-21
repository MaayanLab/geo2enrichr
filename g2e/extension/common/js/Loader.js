
/* A simple loading screen with a cached reference to the DOM element.
 */
var Loader = (function() {

    var $body = $('body'),
        $el = $('' +
            '<div class="g2e-loader-container">' +
                '<div class="g2e-loader-modal">Processing data. This may take a minute.</div>' +
            '</div>'
        );

    return function() {
        return {
            start: function() {
                $body.append($el);
            },
            stop: function() {
                $el.remove();
            }
        };
    };
})();