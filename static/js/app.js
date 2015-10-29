/*
 * Create the App
 */

window.App = Ember.Application.create();

/*
 * Define the router
 */

App.Router.map(function() {
	this.route('about');
	this.resource('pins', function() {
		this.route(':pin_id');
	});
});

