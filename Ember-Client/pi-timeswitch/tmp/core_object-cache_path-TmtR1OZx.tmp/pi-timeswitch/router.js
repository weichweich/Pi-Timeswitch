define('pi-timeswitch/router', ['exports', 'ember', 'pi-timeswitch/config/environment'], function (exports, Ember, config) {

	'use strict';

	var Router = Ember['default'].Router.extend({
		location: config['default'].locationType
	});

	Router.map(function () {
		this.route('about');
		this.route('pins', function () {
			this.route(':pin_id');
		});
	});

	exports['default'] = Router;

});