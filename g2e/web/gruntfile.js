module.exports = function(grunt) {

    var dir = 'extension/js/';

    var src_files = [
        dir + 'config.js',
        dir + 'Comm.js',
        dir + 'Bootstrapper.js',
        dir + 'GdsBootstrapper.js',
        dir + 'GseBootstrapper.js',
        dir + 'G2EComm.js',
        dir + 'LssrComm.js',
        dir + 'Events.js',
        dir + 'TargetApp.js',
        dir + 'Templater.js',
        dir + 'Notifier.js',
        dir + 'BaseScraper.js',
        dir + 'GdsScraper.js',
        dir + 'GseScraper.js',
        dir + 'Ui.js',
        dir + 'main.js'
    ];

    var full_files = [dir + 'open.js'].concat(src_files).concat([dir + 'close.js']);

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
                dest: 'extension/g2e.js',
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.registerTask('build', ['concat', 'jshint']);
};
