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

		let globThis = this
		this.sequenceObserver = {
			objectAdded: (seq: Sequence) => { globThis.addSequence(seq) },
			objectModified: (seq: Sequence) => { globThis.modifySequence(seq) },
			objectRemoved: (seq: Sequence) => { globThis.removeSequence(seq) }
		}
		this.sequenceModel.addObserver(this.sequenceObserver)

		this.pinObserver = {
			objectAdded: (pin: Pin) => {},
			objectModified: (pin: Pin) => { globThis.modifyPin(pin) },
			objectRemoved: (pin: Pin) => { globThis.pinDeleted(pin) }
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
		if (oldVSeq == undefined) {
			throw "Updated sequence not found!"
		} else {
			oldVSeq.sequence.update(sequence)
		}
	}

	public removeSequence = (sequence: Sequence) => {
	    let viewSeqDel = ko.utils.arrayFirst(this.viewSequences(), (viewSeq: ViewSequence) => {
	    	return viewSeq.sequence.id == sequence.id
	    })
	    this.viewSequences.remove(viewSeqDel)
	}

	public pinDeleted = (pin: Pin) => {
		if (pin.id == this.pin().id) {
			this.pushClose(pin)
		}
	}

	public pushEditPin = (params) => {
		if (this.isEditing()) {
			let globThis = this
			this.pinModel.update(this.pin()).then( () => {
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
			this.sequenceModel.update(viewSequence.sequence).then( () => {
				viewSequence.isEditing(!viewSequence.isEditing)
			},(error) => {
				console.log("Error!", error)
			})
		} else {
			viewSequence.isEditing(true)
		}
	}

	public pushClose = (params) => {
		// get the route bevor the current route
		let last_route = this.router.state.routes[this.index]
		this.router.transitionTo(last_route.name)
	}

	public pushRemove = (viewSequence: ViewSequence) => {
		this.sequenceModel.remove(viewSequence.sequence).then((removedSeq: Sequence) => {
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