/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin.ts'
import { Sequence } from '../../model/sequence.ts'
import { Model } from '../../Model'
import router from '../../router.ts'

class ViewModel {
    router: any
    pinModel: Model<Pin>
    sequenceModel: Model<Sequence>
    index: number

    pin: KnockoutObservable<Pin>
    sequences: KnockoutObservableArray<Sequence>

	constructor(params) {
        this.router = params.router
        this.pinModel = params.model.pin
        this.sequenceModel = params.model.sequence
        this.index = params.index

        this.pin = ko.observable(undefined)
        this.sequences = ko.observableArray([])

        this.sequenceModel.addObserver({
            objectAdded: this.addSequence,
            objectModified: this.modifySequence,
            objectRemoved: this.removeSequence
        })

        this.pinModel.addObserver({
            objectAdded: (pin: Pin) => {},
            objectModified: (pin: Pin) => {},
            objectRemoved: this.pinDeleted
        })

        this.pinModel.findOne(params.vals.pinId).then((pin: Pin) => {
            this.pin(pin)
        })
        this.sequenceModel.findAll({
            relation: [{
                type: 'pin',
                id: params.vals.pinId
            }],
            attributes: []
        }).then((sequences: Sequence[]) => {
            this.sequences(sequences)
        })
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
        router.transitionTo('add-sequence', { pinId: this.pin().id })
    }
}

export = ViewModel