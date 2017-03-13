var gulp = require('gulp'),
    debug = require('gulp-debug'),
    filter = require('gulp-filter'),
    browserify = require('browserify'),
    stringify = require('stringify'),
    source = require('vinyl-source-stream')
    connect = require('gulp-connect'),
    proxy = require('http-proxy-middleware'),
    clean = require('gulp-clean'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    watch = require('gulp-watch'),
    addsrc = require('gulp-add-src'),
    tsify = require('tsify');

// static directories
var baseDir = '.',
    srcDir = baseDir + '/src',
    destDir = baseDir + '/build',
    imgSrcDir =  srcDir + '/images',
    compsDir = srcDir + '/components',
    modelDir = srcDir + '/model',
    cssSrcDir = srcDir + '/css',
    cssDestDir = destDir + '/css',
    nodeModulDir = baseDir + '/node_modules',
// static files
    mainFile = 'app.ts',
    indexHTML = 'index.html',
    cssFile = 'styles.css',
    libJSFile = 'libs.js',
    libCSSFile = 'libs.css',
    destFile = 'app.js'
// other
    backendAPI = 'http://localhost:5000';

function swallowError (error) {

  // If you want details of the error in the console
  console.log(error.toString());

  this.emit('end');
}

gulp.copy = function(src, dest){
    return gulp.src(src, {base: srcDir})
        .pipe(gulp.dest(dest));
};

gulp.task('browserify', function() {
    return browserify({
            basedir: srcDir,
            debug: true
        })
    	.transform(stringify(['.html']))
        .add(mainFile)
        .plugin(tsify)
        .bundle()
        .on('error', swallowError)
        .pipe(source(destFile))
        .pipe(gulp.dest(destDir))
        ;
});

gulp.task('copy-index', function() {
    return gulp.copy(srcDir + '/' + indexHTML, destDir)
});

gulp.task('copy-css', function() {
    return gulp.copy(cssSrcDir + '/' + cssFile, destDir)
});

gulp.task('copy-images', function() {
    return gulp.copy(imgSrcDir + '/**/*', destDir)
});

gulp.task('clean', function() {
    return gulp.src(destDir)
        .pipe(clean());
});

gulp.task('build', ['browserify', 'copy-index', 'copy-css', 'copy-images']);

gulp.task('watch', ['build'], function() {
    gulp.watch(imgSrcDir + '/**/*', ['copy-images']);
    gulp.watch(srcDir + '/**/*.js', ['browserify']);
    gulp.watch(srcDir + '/**/*.ts', ['browserify']);
    gulp.watch(srcDir + '/**/*.html', ['browserify']);
    gulp.watch(cssSrcDir + '/**/*', ['copy-css']);
    gulp.watch(srcDir + '/' + indexHTML, ['copy-index']);
});

gulp.task('server', ['build'], function() {
    return connect.server({ 
        root: destDir,
        middleware: function(connect, opt) {
            return [
                proxy('/api', {
                    target: backendAPI,
                    changeOrigin: true
                })
            ]
        }
    });
});

gulp.task('default', ['server', 'watch'])
