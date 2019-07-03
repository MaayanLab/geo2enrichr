module.exports = function(grunt) {

    var WEB = '../g2e/';

    var COMMON = WEB + 'extension/common/';

    var CHROME = WEB + 'extension/chrome/';

    var FIREFOX = WEB + 'extension/firefox/data/';

    var SITE = WEB + 'site/';

    var content_src_files = [
        COMMON + 'js/content_script.js',
        COMMON + 'js/platforms.js',
        COMMON + 'js/Comm.js',
        COMMON + 'js/Page.js',
        COMMON + 'js/UiEmbedder.js',
        COMMON + 'js/EUtilsApi.js',
        COMMON + 'js/Events.js',
        COMMON + 'js/Extension.js',
        COMMON + 'js/Tagger.js',
        COMMON + 'js/Templater.js',
        COMMON + 'js/LoadingScreen.js',
        COMMON + 'js/Notifier.js',
        COMMON + 'js/ScreenScraper.js',
        COMMON + 'js/GdsScraper.js',
        COMMON + 'js/GseScraper.js',
        COMMON + 'js/ModalBox.js',
        COMMON + 'js/UserInputHandler.js',
        COMMON + 'js/main.js'
    ];

    var background_src_files = [
        COMMON + 'js/background.js',
    ];

    var chrome_content_files  = [COMMON + 'js/open.js', COMMON + 'js/config-chrome.js'].concat(content_src_files).concat([COMMON + 'js/close-chrome.js']);
    var chrome_background_files  = [COMMON + 'js/background.js'];

    var firefox_content_files = [COMMON + 'js/open.js', COMMON + 'js/config-firefox.js'].concat(content_src_files).concat([COMMON + 'js/close-firefox.js']);
    var firefox_background_files  = [COMMON + 'js/background.js'];

    var less_files = [COMMON + 'less/*', SITE + 'style/less/*'];

    grunt.initConfig({
        jshint: {
            files: content_src_files,
            options: {
                globals: {
                    jQuery: true
                },
                debug: true
            }
        },
        concat: {
            chrome_content_script: {
                src: chrome_content_files,
                dest: CHROME + 'g2e.js'
            },
            chrome_background_script: {
                src: chrome_background_files,
                dest: CHROME + 'g2e.background.js'
            },
            firefox_content_script: {
                src: firefox_content_files,
                dest: FIREFOX + 'g2e.js'
            },
            firefox_background_script: {
                src: firefox_background_files,
                dest: FIREFOX + 'g2e.background.js'
            }
        },
        less: {
            development: {
                options: {
                    paths: [COMMON + 'less', SITE + 'style/less'],
                    yuicompress: true
                },
                files: {
                    '../g2e/extension/chrome/main.css' : '../g2e/extension/common/less/main.less',
                    '../g2e/extension/firefox/data/main.css': '../g2e/extension/common/less/main.less',
                    '../g2e/site/style/css/main.css'   : '../g2e/site/style/less/main.less'
                }
            }
        },
        watch: {
            files: chrome_content_files.concat(firefox_content_files).concat(less_files),
            tasks: ['build']
        }
    });

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.registerTask('build', ['concat', 'jshint', 'less']);
};
