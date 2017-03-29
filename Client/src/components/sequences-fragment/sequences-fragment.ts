/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model, AppState } from '../../frame'
import { Constants } from '../../config'

class ViewModel {
	router: any
	isEditing: KnockoutObservable<boolean>
	appState: AppState
	pinModel: Model<Pin>
	sequenceModel: Model<Sequence>
	index: number

	pin: KnockoutObservable<Pin>
	sequences: KnockoutObservableArray<Sequence>

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

		this.isEditing = ko.observable(false)
		this.router = appState.router
		this.pinModel = appState.getModel(Constants.model.pin)
		this.sequenceModel = appState.getModel(Constants.model.sequence)
		this.index = viewState.index

		this.pin = ko.observable(undefined)
		this.sequences = ko.observableArray([])

		this.sequenceModel.addObserver({
			objectAdded: this.addSequence,
			objectModified: this.modifySequence,
			objectRemoved: this.removeSequence
		})

		this.pinModel.addObserver({
			objectAdded: (pin: Pin) => {},
			objectModified: this.modifyPin,
			objectRemoved: this.pinDeleted
		})

		this.pinModel.findOne(viewState.route.vals.pinId).then((pin: Pin) => {
		    this.pin(pin)
		})
		this.sequenceModel.findAll({
			relation: [{
				type: Constants.model.pin,
				id: viewState.route.vals.pinId
			}],
			attributes: []
		}).then((sequences: Sequence[]) => {
		    this.sequences(sequences)
		})
	}

	public modifyPin = (pin: Pin) => {
		this.pin().update(pin)
	}

	public addSequence = (sequence: Sequence) => {
	    this.sequences.push(sequence)
	}

	public modifySequence = (sequence: Sequence) => {
		this.removeSequence(sequence)
		this.addSequence(sequence)
	}

	public removeSequence = (sequence: Sequence) => {
	    this.sequences.remove(sequence)
	}

	public pinDeleted = (pin: Pin) => {
		if (pin.id == this.pin().id) {
			this.pushClose(pin)
		}
	}

	public pushEdit = (params) => {
		if (this.isEditing()) {
			let globThis = this
			this.pinModel.update(this.pin(), {
				relation: [],
				attributes: []
			}).then( () => {
				globThis.isEditing(!this.isEditing)
			},(error) => {
				console.log("Error!", error)
			})
		} else {
			this.isEditing(true)
			console.log("push edit!", this.isEditing())
		}
	}

	public pushClose = (params) => {
		// get the route bevor the current route
		let last_route = this.router.state.routes[this.index]
		this.router.transitionTo(last_route.name)
	}

	public pushRemove = (sequence: Sequence) => {
		this.sequenceModel.remove(sequence, {
			relation: [],
			attributes: []
		}).then((removedSeq: Sequence) => {
			this.sequences.remove(removedSeq)
		})
	}

	public pushAdd = (params) => {
		this.router.transitionTo('add-sequence', { pinId: this.pin().id })
	}
}

export = ViewModel