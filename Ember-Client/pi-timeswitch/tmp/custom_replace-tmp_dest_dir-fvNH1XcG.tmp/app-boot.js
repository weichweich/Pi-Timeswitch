/* jshint ignore:start */

define('pi-timeswitch/config/environment', ['ember'], function(Ember) {
  var prefix = 'pi-timeswitch';
/* jshint ignore:start */

try {
  var metaName = prefix + '/config/environment';
  var rawConfig = Ember['default'].$('meta[name="' + metaName + '"]').attr('content');
  var config = JSON.parse(unescape(rawConfig));

  return { 'default': config };
}
catch(err) {
  throw new Error('Could not read config from meta tag with name "' + metaName + '".');
}

/* jshint ignore:end */

});

if (runningTests) {
  require("pi-timeswitch/tests/test-helper");
} else {
  require("pi-timeswitch/app")["default"].create({"name":"pi-timeswitch","version":"0.0.0+"});
}

/* jshint ignore:end */
