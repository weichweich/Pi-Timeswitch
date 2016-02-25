'use strict';


module.exports = function(grunt) {
    grunt.initConfig({
        serve: {
            options: {
                port: 9000,
                'serve': {
                   'path': 'app'
                }
            }
        },
        bower_concat: {
            all: {
                dest: {
                    'js': 'app/build/_bower.js',
                    'css': 'app/build/_bower.css'
                },
                bowerOptions: {
                    relative: false
                },
                mainFiles: {
                    'jQuery': 'dist/jquery.js'
                }
            }
        }    
    });

    grunt.loadNpmTasks('grunt-serve');
    grunt.loadNpmTasks('grunt-bower-concat');
    grunt.registerTask('default', ['bower_concat','serve']);
};
