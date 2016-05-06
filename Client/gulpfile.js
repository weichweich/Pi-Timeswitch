var gulp = require('gulp'),
    debug = require('gulp-debug'),
    filter = require('gulp-filter'),
    browserify = require('browserify'),
    stringify = require('stringify'),
    source = require('vinyl-source-stream')
    mainBowerFiles = require('main-bower-files'),
    connect = require('gulp-connect'),
    proxy = require('http-proxy-middleware'),
    clean = require('gulp-clean'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    watch = require('gulp-watch');

// static directories
var srcDir = './src',
    destDir = './build',
    imgSrcDir =  srcDir + '/images',
    compsDir = srcDir + '/components',
    cssSrcDir = srcDir + '/css',
    cssDestDir = destDir + '/css',
// static files
    mainFile = 'app.js',
    indexHTML = 'index.html',
    cssFile = 'styles.css',
    libJSFile = 'libs.js',
    libCSSFile = 'libs.css',
// other
    backendAPI = 'http://localhost:5000';


gulp.copy=function(src, dest){
    return gulp.src(src, {base: srcDir})
        .pipe(gulp.dest(dest));
};

gulp.task('browserify', function() {
  var bundleMethod = global.isWatching ? watchify : browserify;

  var bundler = bundleMethod({
    // Specify the entry point of your app
    entries: [srcDir + '/' + mainFile]
  });

  var bundle = function() {
    return bundler
      .transform(stringify(['.html']))
      // Enable source maps!
      .bundle()
      // Use vinyl-source-stream to make the
      // stream gulp compatible. Specifiy the
      // desired output filename here.
      .pipe(source(mainFile))
      // Specify the output destination
      .pipe(gulp.dest(destDir));
  };

  return bundle();
});

gulp.task('copy-libs-css', function() {
  var f = filter(['**/*.css']);
  return gulp.src(mainBowerFiles())
    .pipe(f)
    .pipe(gulp.dest(cssDestDir))
});

gulp.task('copy-libs-js', function() {
  var f = filter(['**/*.js'])
  return gulp.src(mainBowerFiles())
    .pipe(f)
    .pipe(concat(libJSFile))
    .pipe(uglify())
    .pipe(gulp.dest(destDir))
});

gulp.task('copy-libs', ['copy-libs-css', 'copy-libs-js']);

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

gulp.task('build', ['browserify', 'copy-index', 'copy-libs', 'copy-css', 'copy-images']);

gulp.task('watch', ['build'], function() {
  gulp.watch(imgSrcDir + '/**/*', ['copy-images']);
  gulp.watch(compsDir + '/**/*', ['browserify']);
  gulp.watch(srcDir + '/*.js', ['browserify']);
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
