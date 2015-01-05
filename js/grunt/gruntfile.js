module.exports = function(grunt) {

	var src_files = [
	    '../config.js',
		'../Comm.js',
		'../Events.js',
		'../Html.js',
		'../Notifier.js',
		'../BaseScraper.js',
		'../GdsScraper.js',
		'../GseScraper.js',
		'../BaseUi.js',
		'../GdsUi.js',
		'../GseUi.js',
		'../main.js'
	];

	var full_files = ['../open.js'].concat(src_files).concat(['../close.js']);

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
				dest: '../../extension/g2e.js',
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-jshint');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.registerTask('build', ['concat', 'jshint']);
};
