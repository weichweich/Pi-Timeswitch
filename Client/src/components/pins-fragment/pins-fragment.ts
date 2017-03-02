/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model } from '../../Model'

class ViewModel {
	router: any
    pinModel: Model<Pin>
    pins: KnockoutObservableArray<Pin>

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

        this.router = appState.router

        this.pinModel = appState.model.pin
        this.pins = ko.observableArray([])

        this.pinModel.addObserver({
            objectAdded: this.addPin,
            objectModified: this.modifyPin,
            objectRemoved: this.removePin
        })

        this.pinModel.findAll({
            relation: [],
            attributes: []
        }).then((pins) => {
            this.pins(pins)
        }).catch((error) => {
			console.log("Error!")
			this.router.transitionTo('login')
		})
    }

    public addPin = (pin: Pin) => {
        this.pins.push(pin)
    }

    public modifyPin = (pin: Pin) => {
        this.removePin(pin)
        this.addPin(pin)
    }

    public removePin = (pin: Pin) => {
        this.pins.remove(pin)
    }

    public pushRemove = (pin: Pin) => {
        this.pinModel.remove(pin, {
            relation: [],
            attributes: []
        })
    }

    public pushAdd = (params) => {
        this.router.transitionTo('add-pin')
    }

    public pushPin = (pin: Pin, event) => {
        this.router.transitionTo('sequences', { pinId: pin.id })
    }

    public dispose = () => {

    }
}

export = ViewModel