/// <reference path="./../typings/main.d.ts" />

import ko = require('knockout')
import router = require('./router')
import { Model } from './model'

ko.components.register('main-page', {
	viewModel: require('./components/main-page/main-page.js'),
	template: require('./components/main-page/main-page.html')
})
ko.components.register('pins-fragment', {
	viewModel: require('./components/pins-fragment/pins-fragment'),
	template: require('./components/pins-fragment/pins-fragment.html')

});
// ko.components.register('sequences-fragment', require('./components/sequences-fragment/sequences-fragment.js'));

ko.components.register('add-pin-fragment', {
	viewModel:	require('./components/add-pin-fragment/add-pin-fragment'),
	template: require('./components/add-pin-fragment/add-pin-fragment.html')
});

// apply the view-model using KnockoutJS as normal
ko.applyBindings({ 
	routeStack: router.currentRouteStack, 
	model: new Model()
});
