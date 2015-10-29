define('pi-timeswitch/components/app-version', ['exports', 'ember-cli-app-version/components/app-version', 'pi-timeswitch/config/environment'], function (exports, AppVersionComponent, config) {

  'use strict';

  var _config$APP = config['default'].APP;
  var name = _config$APP.name;
  var version = _config$APP.version;

  exports['default'] = AppVersionComponent['default'].extend({
    version: version,
    name: name
  });

});