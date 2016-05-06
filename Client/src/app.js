var ko = require('knockout'),
    router = require('./router.js'),
    model = require('./model.js');

ko.components.register('main-page', require('./components/main-page/main-page.js'));
ko.components.register('pins-fragment', require('./components/pins-fragment/pins-fragment.js'));
ko.components.register('sequences-fragment', require('./components/sequences-fragment/sequences-fragment.js'));

ko.components.register('add-pin-fragment', require('./components/add-pin-fragment/add-pin-fragment.js'));

// apply the view-model using KnockoutJS as normal
ko.applyBindings({ 
	routeStack: router.currentRouteStack, 
	model: model
});
