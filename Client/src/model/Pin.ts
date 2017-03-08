/// <reference path="./../../typings/main.d.ts" />

import ko = require('knockout')

import { Identifiable } from '../frame'

export let definition = {
	name: '',
	state: '',
	number: '',
	sequences: {
		jsonApi: 'hasMany',
		type: 'sequences'
	}
}

export let parser = {
	jsonToObject: jsonToPin,
	objectToJson: pinToJson
}

export interface PinJson {
	id: number

	name: string
	number: number
	state: number
}

export function jsonToPin(json: any): Pin {
	return new Pin(json.id, json.number, json.name, json.state)
}

export function pinToJson(pin: Pin) {
	return {
		id: pin.id,
		name: ko.utils.unwrapObservable(pin.name),
		number: ko.utils.unwrapObservable(pin.number),
		state: ko.utils.unwrapObservable(pin.state)
	}
}

let images=[
	'images/off.png',
	'images/on.png',
	'images/undef.png'
]

export class Pin {
	public static readonly OFF=0
	public static readonly ON=1
	public static readonly UNDEF=2
	id: number

	number: KnockoutObservable<number>
	name: KnockoutObservable<string>
	state: KnockoutObservable<number>
	stateImage: KnockoutObservable<string>

	constructor(anID: number, aNumber: number, aName: string, aState: number) {
		this.id = anID
		this.number = ko.observable(aNumber)
		this.name = ko.observable(aName)
		this.state = ko.observable(aState)
		this.stateImage = ko.computed(() => {
			return images[this.state()]
		})
	}
}
