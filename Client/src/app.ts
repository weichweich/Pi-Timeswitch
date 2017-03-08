/// <reference path="./../typings/main.d.ts" />

import ko = require('knockout')
import { Model, startApp } from './frame'
import { Constants } from './config'

import * as pin from './model/pin'
import * as seq from './model/Sequence'
import { AppState } from "./AppState"

// ************** Register Components **************

console.log('Register Componentes')

ko.components.register('header', {
	viewModel: require('./components/header/header'),
	template: require('./components/header/header.html')
})
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
})
ko.components.register('sequences-fragment', {
	viewModel: require('./components/sequences-fragment/sequences-fragment'),
	template: require('./components/sequences-fragment/sequences-fragment.html')
})
ko.components.register('add-pin-fragment', {
	viewModel: require('./components/add-pin-fragment/add-pin-fragment'),
	template: require('./components/add-pin-fragment/add-pin-fragment.html')
})
ko.components.register('add-sequence-fragment', {
	viewModel: require('./components/add-sequence-fragment/add-sequence-fragment'),
	template: require('./components/add-sequence-fragment/add-sequence-fragment.html')
})

// ************** Start App **************

console.log('Start App')

let appState = startApp()

// ************** Register Model **************

console.log('Register Models')

let sequenceModel = new Model<seq.Sequence>(Constants.model.sequence, seq.definition, {}, seq.parser)
let pinModel = new Model<pin.Pin>(Constants.model.pin, pin.definition, {}, pin.parser)

appState.setModel(Constants.model.pin, pinModel)
appState.setModel(Constants.model.sequence, sequenceModel)
