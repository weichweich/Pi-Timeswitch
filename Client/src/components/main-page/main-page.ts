/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model, AppState } from '../../frame'
import { Constants } from '../../config'

class ViewModel {
	router: any
	pinModel: Model<Pin>
	index: number
	appState: AppState

	title: KnockoutObservable<string>
	pins: KnockoutObservableArray<Pin>
	pinsOn: KnockoutComputed<Pin[]>

	constructor(params) {
		let viewState = params.viewState
		let appState: AppState = params.appState

		this.router = appState.router
		this.index = viewState.index
		this.pinModel = appState.getModel(Constants.model.pin)

		this.pins = ko.observableArray([])
		this.pinsOn = ko.computed({
    	    owner: this,
    	    read:  () => {
    	        return this.pins().filter((pin: Pin, i: number) => {
    	        	return pin.state() == Pin.ON
    	        })
    	    }
    	});
		this.title = ko.observable('Overview!')

		this.pinModel.findAll({
			relation: [],
			attributes: []
		}).then((pins) => {
			console.log("Pins!", pins)
			this.pins(pins)
		}, (error) => {
			console.log("Error!", error)
			this.router.transitionTo('login', { backRoute: this.router.state.path })
		})
	}
};

export = ViewModel