/// <reference path="./../../typings/main.d.ts" />

import ko = require('knockout')

import { Identifiable } from './Interfaces.ts'

export interface PinJson {
	id: number

	name: string
	number: number
	state: number
}

export function jsonToPin(json) {
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

export class Pin {
	id: number

	number: KnockoutObservable<number>
	name: KnockoutObservable<string>
	state: KnockoutObservable<number>

	constructor(anID: number, aNumber: number, aName: string, aState: number) {
		this.id = anID
		this.number = ko.observable(aNumber)
		this.name = ko.observable(aName)
		this.state = ko.observable(aState)
	}
}
