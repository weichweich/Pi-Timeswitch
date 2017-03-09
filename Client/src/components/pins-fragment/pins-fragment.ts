/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model } from '../../frame'
import { AppState } from '../../AppState'
import { Constants } from '../../config'

class ViewModel {
	router: any
    pinModel: Model<Pin>
    pins: KnockoutObservableArray<Pin>
    appState: AppState

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

        this.router = appState.router

        this.pinModel = appState.getModel(Constants.model.pin)
        this.pins = ko.observableArray([])

        this.pinModel.addObserver({
            objectAdded: this.addPin,
            objectModified: this.modifyPin,
            objectRemoved: this.removePin
        })

        let globThis = this
        this.pinModel.findAll({
            relation: [],
            attributes: []
        }).then((pins) => {
            this.pins(pins)
        }, (error) => {
            console.log("Error!")
            globThis.router.transitionTo('login', { 
                backRoute: globThis.router.state.path 
            })
        })
    }

    public addPin = (pin: Pin) => {
        this.pins.push(pin)
    }

    public modifyPin = (pin: Pin) => {
    	var oldPin = ko.utils.arrayFirst(this.pins(), (testPin: Pin) => {
    		return testPin.id == pin.id
    	})
    	if (!oldPin) {
    		throw "Updated pin not found!"
    	} else {
    		oldPin.update(pin)
    	}
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

    public pushSwitchState = (pin: Pin, event) => {
    	let pinCopy = pin.copy()
    	pin.state(Pin.UNDEF)
    	if (pinCopy.state() == Pin.ON) {
    		pinCopy.state(Pin.OFF)
    	} else if (pinCopy.state() == Pin.OFF) {
    		pinCopy.state(Pin.ON)
    	}
        let globThis = this
    	this.pinModel.update(pinCopy, {
           relation: [],
            attributes: []
    	}).catch((error) => {
            console.log("Error!", error)
    	})
    }
}

export = ViewModel