/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')
import $ = require('jquery')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model } from '../../Model'

class ViewModel {
	router: any
	index: number
	appState: any

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
		let data = {
			'name': this.name(),
			'password': this.password()
		}
		let glob_this = this;
		$.ajax({
			url: "api/login",
			type: "POST",
			data: JSON.stringify(data),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
		}).done(function(data) {
			let jsonObj = JSON.parse(data)
			console.log(jsonObj['token'])
			glob_this.appState.login_func(jsonObj['token'])
			glob_this.router.transitionTo('/')
		}).fail(function(data) {
			console.log( "error", data)
		});
	}
}

export = ViewModel