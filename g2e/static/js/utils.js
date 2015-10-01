function Loader(message) {
    var message = message || 'Loading...',
        $el = $('<div class="loading"><div class="loader"><div class="modal">' + message + '</div></div></div>');
    return {
        start: function() {
            $('body').append($el);
        },
        stop: function() {
            $el.remove();
        }
    }
}