/// <reference path="./../../typings/main.d.ts" />

import ko = require('knockout')

import { Sequence, SequenceJson } from './sequence.ts'

export class Pin {
	id: number

	number: KnockoutObservable<number>
	name: KnockoutObservable<string>
	state: KnockoutObservable<number>
	sequences: KnockoutObservableArray<Sequence>

	constructor(anID: number, aNumber: number, aName: string, aState: number, aSequenceList: Sequence[]) {
		this.id = anID
		this.number = ko.observable(aNumber)
		this.name = ko.observable(aName)
		this.state = ko.observable(aState)
		
		if (!aSequenceList) {
			this.sequences = ko.observableArray([])
		} else {
			this.sequences = ko.observableArray(aSequenceList)
		}

	}
}