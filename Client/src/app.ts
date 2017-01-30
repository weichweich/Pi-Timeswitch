/// <reference path="./../typings/main.d.ts" />

import ko = require('knockout')
import router from './router.ts'
import { Model } from './model'

import { Pin, PinJson, pinToJson, jsonToPin } from './model/pin.ts'
import { Sequence, SequenceJson, sequenceToJson, jsonToSequence } from './model/Sequence.ts'

// ************** Setup Router **************

// observable array of current displayed routes
let currentRouteStack = ko.observableArray([])

router.use(function(transition, nextRouteStack){
	// swap next route stack with current stack
	console.log("RouteStack: ", nextRouteStack)
	currentRouteStack(nextRouteStack)
})

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
let sequenceModel = new Model<Sequence>('sequence', sequenceDef, {}, sequenceParser)

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
let pinModel = new Model<Pin>('pin', pinDef, {}, pinParser)


// ************** Register Components **************

ko.components.register('main-page', {
	viewModel: require('./components/main-page/main-page.js'),
	template: require('./components/main-page/main-page.html')
})
ko.components.register('pins-fragment', {
	viewModel: require('./components/pins-fragment/pins-fragment'),
	template: require('./components/pins-fragment/pins-fragment.html')

});
ko.components.register('sequences-fragment', {
	viewModel: require('./components/sequences-fragment/sequences-fragment.ts'),
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
