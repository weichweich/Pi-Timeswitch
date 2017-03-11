/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')
import { User } from '../../model/user'
import { Model } from '../../frame'
import { AppState } from '../../AppState'
import { Constants } from '../../config'

class ViewModel {
	router: any
    appState: AppState
	userModel: Model<User>
	name: KnockoutObservable<string>
	privilege: KnockoutObservable<string>
	password: KnockoutObservable<string>
	email: KnockoutObservable<string>
	state: KnockoutObservable<string>

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState
		this.router = appState.router
        this.userModel = appState.getModel(Constants.model.user)
		this.name = ko.observable('')
		this.privilege = ko.observable('')
		this.password = ko.observable('')
		this.email = ko.observable('')
		this.state = ko.observable('ready') // possible: ready, uploading 
	}

	public cancle (params) {
		// length of current route stack
		let length = this.router.state.routes.length
		// get the route bevor the current route
		let last_route = this.router.state.routes[length-2]
		this.router.transitionTo(last_route.name)
	}

	public addUser (params) {
		if (this.state() !== 'ready') {
			return
		}

		this.stateUploading()

		let aName = ko.utils.unwrapObservable(this.name)
		let aPrivilege = ko.utils.unwrapObservable(this.privilege)
		let anEmail = ko.utils.unwrapObservable(this.email)
		let password = ko.utils.unwrapObservable(this.password)

		let user = new User(-1, aName, aPrivilege, anEmail)
		user.password(password)

		this.userModel.create(user, {
			relation: [],
			attributes: []
		}).then((respons) => {
			user.password('')
			this.name('')
			this.privilege('')
			this.email('')
			this.password('')
			this.stateReady()
		}, (error) => {
			this.stateReady()
			console.log(error)
		})
	}

	public stateUploading () {
		this.state('uploading')
	}
	public stateReady () {
		this.state('ready')
	}
}

export = ViewModel
