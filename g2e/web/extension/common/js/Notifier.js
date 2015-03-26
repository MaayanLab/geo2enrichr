
var Notifier = function(DEBUG) {

	var log = function(msg) {
		if (DEBUG) {
			console.log(msg);
		}
	};

	var warn = function(msg) {
		alert(msg);
	};

	return {
		log: log,
		warn: warn
	};
};
