/// <reference path="./../typings/main.d.ts" />

let _ = require('lodash')
import ko = require('knockout')
import router from './router'
import { Model } from './model'

import { Pin, PinJson, pinToJson, jsonToPin } from './model/pin'
import { Sequence, SequenceJson, sequenceToJson, jsonToSequence } from './model/Sequence'

// ************** Define Model **************

let sequenceDef = {
	start_time: '',
	start_range: '',
	end_time: '',
	end_range: '',
	pin_id: ''
}
let sequenceParser = { 
	jsonToObject: jsonToSequence, 
	objectToJson: sequenceToJson
}
let sequenceModel: Model<Sequence> = new Model<Sequence>('sequence', sequenceDef, {}, sequenceParser)

let pinDef = {
	name: '',
	state: '',
	number: '',
	sequences: {
		jsonApi: 'hasMany',
		type: 'sequences'
	}
}
let pinParser = {
	jsonToObject: jsonToPin,
	objectToJson: pinToJson
}
let pinModel: Model<Pin> = new Model<Pin>('pin', pinDef, {}, pinParser)

// ************** Setup Router **************

let appState = {
	router: router,
	model: {
		sequence: sequenceModel,
		pin: pinModel
	},
	login_func: (token: string) => {
		sequenceModel.connection.setJWTToken(token)
		pinModel.connection.setJWTToken(token)
	}
}

// observable array of current displayed routes
let currentRouteStack = ko.observableArray([])

// routes are extended with global obejcts and route specific properties:
// router, view state, application state
router.use(function(transition, nextRouteStack){
	// update the currentRouteStack to macht the nextRouteStack
	let remove_count = currentRouteStack().length - nextRouteStack.length
	if (remove_count > 0) {
		currentRouteStack.splice(nextRouteStack.length, remove_count)
	}

	for (var _i = 0; _i < nextRouteStack.length; _i++) {
		let newRoute = {
			viewState: {
				index: _i,
				route: nextRouteStack[_i]
			},
			appState: appState
		} 

		if (currentRouteStack().length <= _i) {
			// current route stack is shorter 
			currentRouteStack.push(newRoute)

		} else if (!_.isEqual(newRoute, currentRouteStack()[_i])) {
			// if routes are not equal, replace with new one
			currentRouteStack()[_i] = newRoute

			// remove all routes after the current item on current stack
			// stack: [0, ..., _i, ... remove ...]
			if (currentRouteStack().length > _i) {
				let remove_count = currentRouteStack().length -_i -1
				currentRouteStack.splice(_i, remove_count)
			}
		}
	}
})

// ************** Register Components **************

ko.components.register('login-page', {
	viewModel: require('./components/login-page/login-page'),
	template: require('./components/login-page/login-page.html')
})
ko.components.register('main-page', {
	viewModel: require('./components/main-page/main-page'),
	template: require('./components/main-page/main-page.html')
})
ko.components.register('pins-fragment', {
	viewModel: require('./components/pins-fragment/pins-fragment'),
	template: require('./components/pins-fragment/pins-fragment.html')

});
ko.components.register('sequences-fragment', {
	viewModel: require('./components/sequences-fragment/sequences-fragment'),
	template: require('./components/sequences-fragment/sequences-fragment.html')
});

ko.components.register('add-pin-fragment', {
	viewModel: require('./components/add-pin-fragment/add-pin-fragment'),
	template: require('./components/add-pin-fragment/add-pin-fragment.html')
});
ko.components.register('add-sequence-fragment', {
	viewModel: require('./components/add-sequence-fragment/add-sequence-fragment'),
	template: require('./components/add-sequence-fragment/add-sequence-fragment.html')
});

// ************** Set Root ViewModel **************

ko.applyBindings({ 
	routeStack: currentRouteStack, 
	model: {
		sequence: sequenceModel,
		pin: pinModel
	},
	router: router
});
