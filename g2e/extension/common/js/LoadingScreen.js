
/* A simple loading screen with a configurable message.
 */
function LoadingScreen(message) {

    var $body = $('body'),
        $el = $('' +
            '<div class="g2e-loader-container">' +
                '<div class="g2e-loader-modal">' + message + '</div>' +
            '</div>'
        );

    return {
        start: function() {
            $body.append($el);
        },
        stop: function() {
            $el.remove();
        }
    };
}