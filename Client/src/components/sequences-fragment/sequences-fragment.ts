/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model, AppState, Observer } from '../../frame'
import { Constants } from '../../config'

class ViewSequence {
	public isEditing: KnockoutObservable<boolean>
	public sequence: Sequence

	constructor(newSequence: Sequence) {
		this.isEditing = ko.observable(false)
		this.sequence = newSequence
	}

}

class ViewModel {
	router: any
	isEditing: KnockoutObservable<boolean>
	appState: AppState
	pinModel: Model<Pin>
	sequenceModel: Model<Sequence>
	index: number

	pin: KnockoutObservable<Pin>
	viewSequences: KnockoutObservableArray<ViewSequence>

	pinObserver: Observer<Pin>
	sequenceObserver: Observer<Sequence>

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

		this.isEditing = ko.observable(false)
		this.router = appState.router
		this.pinModel = appState.getModel(Constants.model.pin)
		this.sequenceModel = appState.getModel(Constants.model.sequence)
		this.index = viewState.index

		this.pin = ko.observable(undefined)
		this.viewSequences = ko.observableArray([])

		this.sequenceObserver = {
			objectAdded: this.addSequence,
			objectModified: this.modifySequence,
			objectRemoved: this.removeSequence
		}
		this.sequenceModel.addObserver(this.sequenceObserver)

		this.pinObserver = {
			objectAdded: (pin: Pin) => {},
			objectModified: this.modifyPin,
			objectRemoved: this.pinDeleted
		}
		this.pinModel.addObserver(this.pinObserver)

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
			this.viewSequences(sequences.map((seq: Sequence, i: number) => {
				return new ViewSequence(seq)
			}))
		})
	}

	public modifyPin = (pin: Pin) => {
		if (this.pin() && this.pin().id == pin.id) {
			this.pin().update(pin)
		} else {
			console.log("wrong pin")
		}
	}

	public addSequence = (sequence: Sequence) => {
	    this.viewSequences.push(new ViewSequence(sequence))
	}

	public modifySequence = (sequence: Sequence) => {
		var oldVSeq = ko.utils.arrayFirst(this.viewSequences(), (testVSeq: ViewSequence) => {
			return testVSeq.sequence.id == sequence.id
		})
		if (!oldVSeq) {
			throw "Updated sequence not found!"
		} else {
			oldVSeq.sequence.update(sequence)
		}
	}

	public removeSequence = (sequence: Sequence) => {
	    this.viewSequences.remove(new ViewSequence(sequence))
	}

	public pinDeleted = (pin: Pin) => {
		if (pin.id == this.pin().id) {
			this.pushClose(pin)
		}
	}

	public pushEditPin = (params) => {
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
		}
	}

	public pushEditSequence = (viewSequence: ViewSequence) => {
		if (viewSequence.isEditing()) {
			let globThis = this
			this.sequenceModel.update(viewSequence.sequence, {
				relation: [],
				attributes: []
			}).then( () => {
				viewSequence.isEditing(!viewSequence.isEditing)
			},(error) => {
				console.log("Error!", error)
			})
		} else {
			viewSequence.isEditing(true)
			console.log("push edit!", viewSequence)
		}
	}

	public pushClose = (params) => {
		// get the route bevor the current route
		let last_route = this.router.state.routes[this.index]
		this.router.transitionTo(last_route.name)
	}

	public pushRemove = (viewSequence: ViewSequence) => {
		this.sequenceModel.remove(viewSequence.sequence, {
			relation: [],
			attributes: []
		}).then((removedSeq: Sequence) => {
			this.viewSequences.remove(new ViewSequence(removedSeq))
		})
	}

	public pushAdd = (params) => {
		this.router.transitionTo('add-sequence', { pinId: this.pin().id })
	}

	public dispose = () => {
		this.pinModel.removeObserver(this.pinObserver)
		this.sequenceModel.removeObserver(this.sequenceObserver)
	}
}

export = ViewModel