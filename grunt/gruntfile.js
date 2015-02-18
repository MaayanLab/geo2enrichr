module.exports = function(grunt) {

	var src_files = [
	    '../extension/js/config.js',
		'../extension/js/Comm.js',
        '../extension/js/Bootstrapper.js',
		'../extension/js/GdsBootstrapper.js',
		'../extension/js/GseBootstrapper.js',
		'../extension/js/G2EComm.js',
		'../extension/js/LssrComm.js',
		'../extension/js/Events.js',
		'../extension/js/TargetApp.js',
		'../extension/js/Templater.js',
		'../extension/js/Notifier.js',
		'../extension/js/BaseScraper.js',
		'../extension/js/GdsScraper.js',
		'../extension/js/GseScraper.js',
		'../extension/js/Ui.js',
		'../extension/js/main.js'
	];

	var full_files = ['../extension/js/open.js'].concat(src_files).concat(['../extension/js/close.js']);

	grunt.initConfig({
		jshint: {
			files: src_files,
			options: {
				globals: {
					jQuery: true
				},
				debug: true
			}
		},
		watch: {
			files: full_files,
			tasks: ['build']
		},
		concat: {
			dist: {
				src: full_files,
				dest: '../extension/g2e.js',
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-jshint');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.registerTask('build', ['concat', 'jshint']);
};
