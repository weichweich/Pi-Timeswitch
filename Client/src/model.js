var JsonApiDataStore = require('jsonapi-datastore'),
	$ = require('jQuery'),
	config = require('./config.js');

var store = new JsonApiDataStore();

var model = {
	pullAll: function(type, callbacks) {
		$.getJSON(config.backendURL + '/' + type)
			.done(function(data) {
				store.sync(data);
				callbacks();
			});
	},
	pull: function(type, id, callbacks) {
		$.getJSON(config.backendURL + '/' + type + '/' + id)
			.done(function(data) {
				store.sync(data);
				callbacks();
			});
	},
	pushAll: function(type, object, callbacks) {

	},
	push: function(type, id, object, callbacks) {

	}
}

module.exports = {
  store: store,
  model: model
};  