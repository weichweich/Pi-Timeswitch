/// <reference path="./../typings/main.d.ts" />

import config = require('./config')

import $ = require('jquery')
import ko = require('knockout')
var JsonApi = require('devour-client')
import promise = require('ts-promise')
let Promise = promise.Promise

import { Pin } from './model/pin.ts'
import { Sequence } from './model/sequence.ts'


export class Model {

	jsonApi: any

	pins: KnockoutObservableArray<Pin>

	constructor() {
		this.jsonApi = new JsonApi({ apiUrl: config.backendURL })
		this.pins = ko.observableArray([])
		this.pins.subscribe(() => {
            console.log('got it! Model')
        })
		this.jsonApi.define('pin', {
			name: '',
			number: '',
			state: '',
			sequences: {
				jsonApi: 'hasMany',
				type: 'sequence'
			}
		}, {})

		this.jsonApi.define('sequence', {
			start_time: '',
			start_range: '',
			end_time: '',
			end_range: '',
		}, {})

		this.findPins().then((newPins) => {
			this.pins(newPins)
		})
	}

	jsonToPin(json) {
		let sequences: Sequence[] = []
		if ('sequences' in json)
			for (let sequence of <any[]>json.sequences) {
				let sequenceObj = new Sequence(sequence.id, sequence.start_time, sequence.start_range,
					sequence.end_time, sequence.end_range)

				sequences.push(sequenceObj)
			}

		return new Pin(json.id, json.number, json.name, json.state, sequences)
	}

	pinToJSON(pin: Pin) {
		let jsonSequences = []
		for (let sequence of pin.sequences()) {
			jsonSequences.push(this.sequenceToJSON(sequence))
		}
		return {
			id: pin.id,
			name: ko.utils.unwrapObservable(pin.name),
			number: ko.utils.unwrapObservable(pin.number),
			state: ko.utils.unwrapObservable(pin.state),
			sequences: jsonSequences
		}
	}

	sequenceToJSON(sequence: Sequence) {
		return {}
	}

	public findPins = () => {
		return this.jsonApi.findAll('pins')
			.then((data: any[]) => {

				// then: convert raw pins to Pin-objects
				let pins: Pin[] = []
				for (let json of data) {
					pins.push(this.jsonToPin(json))
				}
				console.log(pins)
				return pins
			}, (data) => { return data })
	}

	public updatePins = (pins: Pin[]) => {
		return this.jsonApi.update('pin', pins)
	}

	public deletePin = (pin: Pin) => {
		return this.jsonApi.destroy('pin', pin.id)
			.then((respons) => {
				let index = this.pins().indexOf(pin, 0);
				if (index > -1) {
					this.pins.splice(index, 1);
				}
			})
	}

	public createPin = (pin: Pin) => {
		let jsonPin = this.pinToJSON(pin)

		console.log(jsonPin)
		return this.jsonApi.create('pin', jsonPin).then((serverPin) => {
			let pin = this.jsonToPin(serverPin)
			this.pins.push(pin)
		})
	}
}

