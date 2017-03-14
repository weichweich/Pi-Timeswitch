/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model, AppState } from '../../frame'

class ViewModel {
	router: any
	index: number
	appState: AppState

	name: KnockoutObservable<string>
	password: KnockoutObservable<string>

	constructor(params) {
		let viewState = params.viewState
		this.appState = params.appState
		
		this.name = ko.observable('')
		this.password = ko.observable('')

		this.router = this.appState.router
		this.index = viewState.index
	}

	public pushLogin = (param: any) => {
		console.log('push login')
		let globThis = this
		this.appState.login(this.name(), this.password())
					 .then(function(data) {
			globThis.router.transitionTo('/')
		})
	}
}

export = ViewModel