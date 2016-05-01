var gulp = require('gulp'),
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
    imgDir =  srcDir + '/images',
    compsDir = srcDir + '/components'
// static files
    mainFile = 'app.js',
    indexHTML = 'index.html',
    cssFile = 'css/styles.css',
    libFile = 'libs.js'
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

gulp.task('copy-libs', function() {
  return gulp.src(mainBowerFiles())
    .pipe(concat(libFile))
    .pipe(uglify())
    .pipe(gulp.dest(destDir))
});

gulp.task('copy-index', function() {
  return gulp.copy(srcDir + '/' + indexHTML, destDir)
});

gulp.task('copy-css', function() {
  return gulp.copy(srcDir + '/' + cssFile, destDir)
});

gulp.task('copy-images', function() {
  return gulp.copy(srcDir + '/' + imgDir + '/**/*', destDir)
});

gulp.task('clean', function() {
    return gulp.src(destDir)
      .pipe(clean());
});

gulp.task('build', ['browserify', 'copy-index', 'copy-libs', 'copy-css', 'copy-images']);

gulp.task('watch', ['build'], function() {
  gulp.watch(imgDir, ['copy-images']);
  gulp.watch(compsDir + '/**/*', ['browserify']);
  gulp.watch(cssFile, ['copy-css']);
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
