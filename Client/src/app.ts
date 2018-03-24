/// <reference path="./../typings/main.d.ts" />

import ko = require('knockout')
import { Model, startApp, AppState } from './frame'
import { Constants } from './config'

import * as pin from './model/Pin'
import * as seq from './model/Sequence'
import * as user from './model/User'

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
ko.components.register('users-fragment', {
	viewModel: require('./components/users-fragment/users-fragment'),
	template: require('./components/users-fragment/users-fragment.html')
})
ko.components.register('add-user-fragment', {
	viewModel: require('./components/add-user-fragment/add-user-fragment'),
	template: require('./components/add-user-fragment/add-user-fragment.html')
})
ko.components.register('user-fragment', {
	viewModel: require('./components/user-fragment/user-fragment'),
	template: require('./components/user-fragment/user-fragment.html')
})
ko.components.register('pins-fragment', {
	viewModel: require('./components/pins-fragment/pins-fragment'),
	template: require('./components/pins-fragment/pins-fragment.html')
})
ko.components.register('add-pin-fragment', {
	viewModel: require('./components/add-pin-fragment/add-pin-fragment'),
	template: require('./components/add-pin-fragment/add-pin-fragment.html')
})
ko.components.register('sequences-fragment', {
	viewModel: require('./components/sequences-fragment/sequences-fragment'),
	template: require('./components/sequences-fragment/sequences-fragment.html')
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
let userModel = new Model<user.User>(Constants.model.user, user.definition, {}, user.parser)

appState.setModel(Constants.model.pin, pinModel)
appState.setModel(Constants.model.sequence, sequenceModel)
appState.setModel(Constants.model.user, userModel)
