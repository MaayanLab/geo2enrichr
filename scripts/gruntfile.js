module.exports = function(grunt) {

    var WEB = '../g2e/web/';

    var EXTENSION = WEB + 'extension/';

    var SITE = WEB + 'site/';

    var JS_DIR = EXTENSION + 'js/';

    var src_files = [
        JS_DIR + 'config.js',
        JS_DIR + 'Comm.js',
        JS_DIR + 'Bootstrapper.js',
        JS_DIR + 'GdsBootstrapper.js',
        JS_DIR + 'GseBootstrapper.js',
        JS_DIR + 'G2EComm.js',
        JS_DIR + 'LssrComm.js',
        JS_DIR + 'Events.js',
        JS_DIR + 'TargetApp.js',
        JS_DIR + 'Templater.js',
        JS_DIR + 'Notifier.js',
        JS_DIR + 'BaseScraper.js',
        JS_DIR + 'GdsScraper.js',
        JS_DIR + 'GseScraper.js',
        JS_DIR + 'Ui.js',
        JS_DIR + 'main.js'
    ];

    var js_files = [JS_DIR + 'open.js'].concat(src_files).concat([JS_DIR + 'close.js']);

    var less_files = [EXTENSION + 'less/*', SITE + 'style/less/*'];

    var full_files = js_files.concat(less_files);

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
        concat: {
            dist: {
                src: js_files,
                dest: EXTENSION + 'g2e.js',
            }
        },
        less: {
            development: {
                options: {
                    paths: [EXTENSION + 'less', SITE + 'style/less'],
                    yuicompress: true
                },
                files: {
                    '../g2e/web/extension/css/main.css': '../g2e/web/extension/less/main.less',
                    '../g2e/web/site/style/css/main.css' : '../g2e/web/site/style/less/main.less'
                }
            }
        },
        watch: {
            files: full_files,
            tasks: ['build']
        }
    });

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.registerTask('build', ['concat', 'jshint', 'less']);
};