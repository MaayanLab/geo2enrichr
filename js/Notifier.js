
var Notifier = function(DEBUG) {

	var log = function(msg) {
		if (DEBUG) {
			console.log(msg);
		}
	};

	var ask = function(msg, deflt) {
		return prompt(msg, deflt);
	};

	var warn = function(msg) {
		alert(msg);
	};

	return {
		log: log,
		ask: ask,
		warn: warn
	};
};
