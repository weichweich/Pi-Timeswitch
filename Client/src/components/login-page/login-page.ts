/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model, AppState } from '../../frame'

interface Error {
	title: KnockoutObservable<string>
	detail: KnockoutObservable<string>
	code: KnockoutObservable<number>
}

class ViewModel {
	router: any
	index: number
	appState: AppState

	name: KnockoutObservable<string>
	password: KnockoutObservable<string>

	error: KnockoutObservable<Error>

	constructor(params) {
		let viewState = params.viewState
		this.appState = params.appState
		
		this.name = ko.observable('')
		this.password = ko.observable('')

		this.router = this.appState.router
		this.index = viewState.index

		this.error = ko.observable(undefined)
	}

	public pushLogin = (param: any) => {
		console.log('push login')
		let globThis = this
		this.appState.login(this.name(), this.password())
					 .then((data) => {
			globThis.router.transitionTo('/')
		}, (error) => {
			console.log("Login Comp", error)
			globThis.error(error)
		})
	}
}

export = ViewModel