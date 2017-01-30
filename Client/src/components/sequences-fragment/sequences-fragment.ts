/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin.ts'
import { Sequence } from '../../model/sequence.ts'
import { Model } from '../../Model'
import router from '../../router.ts'

class ViewModel {
    pinModel: Model<Pin>
    sequenceModel: Model<Sequence>

    pin: KnockoutObservable<Pin>
    sequences: KnockoutObservableArray<Sequence>

	constructor(params) {
        this.pinModel = params.model.pin
        this.sequenceModel = params.model.sequence

        this.pin = ko.observable(undefined)
        this.sequences = ko.observableArray([])

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
            console.log("sequences", sequences)
            this.sequences(sequences)
        })
	}

    public remove = (sequence: Sequence) => {
        this.sequenceModel.remove(sequence, {
            relation: [],
            attributes: []
        }).then((removedSeq: Sequence) => {
            this.sequences.remove(removedSeq)
        })    	
    }

    public showAdd = (params) => {
        router.transitionTo('add-sequence', { pinId: this.pin().id })
    }
}

export = ViewModel