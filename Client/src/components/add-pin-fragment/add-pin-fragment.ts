/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')
import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model, ErrorDescriptor, AppState } from '../../frame'
import { Constants } from '../../config'

class ViewModel {
	router: any
    appState: AppState
	pinModel: Model<Pin>
	name: KnockoutObservable<string>
	number: KnockoutObservable<number>
	state: KnockoutObservable<string>

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState
		this.router = appState.router
        this.pinModel = appState.getModel(Constants.model.pin)
		this.name = ko.observable('')
		this.number = ko.observable(0)
		this.state = ko.observable('ready') // possible: ready, uploading 
	}

	public cancle (params) {
		// length of current route stack
		let length = this.router.state.routes.length
		// get the route bevor the current route
		let last_route = this.router.state.routes[length-2]
		this.router.transitionTo(last_route.name)
	}

	public addPin (params) {
		if (this.state() !== 'ready') {
			return
		}

		this.stateUploading()

		let aName = ko.utils.unwrapObservable(this.name)
		let aNumber = ko.utils.unwrapObservable(this.number)

		let pin = new Pin(aNumber, aNumber, aName, 0)
		let globThis = this
		this.pinModel.create(pin, {
			relation: [],
			attributes: []
		}).then((respons) => {
			this.name('')
			this.number(0)
			this.stateReady()
		}, (error) => { 
			this.name('')
			this.number(0)
			this.stateReady()
			if (error.code == 401) {
				globThis.router.transitionTo('login', { 
				    backRoute: globThis.router.state.path 
				})
			} else {
				console.log("Error!", error)
			}
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
