/// <reference path="./../../typings/main.d.ts" />

import ko = require('knockout')

import { Identifiable } from '../frame'

export let definition = {
	start_time: '',
	start_range: '',
	end_time: '',
	end_range: '',
	pin_id: ''
}

export let parser = { 
	jsonToObject: jsonToSequence, 
	objectToJson: sequenceToJson
}

export interface SequenceJson extends Identifiable {
	id: number
	pin_id: number

	start_time: string
	start_range: string

	end_time: string
	end_range: string
}

export class Sequence implements Identifiable {
	id: number
	pin_id: number

	start_time: KnockoutObservable<string>
	start_range: KnockoutObservable<string>

	end_time: KnockoutObservable<string>
	end_range: KnockoutObservable<string>

	constructor(anID: number, pinId: number, aStart_time: string, aStart_range: string, anEnd_time: string, anEnd_range: string) {
		this.id = anID
		this.pin_id = pinId

		this.start_time = ko.observable(aStart_time)
		this.start_range = ko.observable(aStart_range)

		this.end_time = ko.observable(anEnd_time)
		this.end_range = ko.observable(anEnd_range)
	}
}

export function sequenceToJson(sequence: Sequence): SequenceJson {
	return {
		id: sequence.id,
		pin_id: sequence.pin_id,
		start_time: ko.utils.unwrapObservable(sequence.start_time),
		start_range: ko.utils.unwrapObservable(sequence.start_range),
		end_time: ko.utils.unwrapObservable(sequence.end_time),
		end_range: ko.utils.unwrapObservable(sequence.end_range)
	}
}

export function jsonToSequence(sequence: SequenceJson): Sequence {
	return new Sequence(
		sequence.id,
		sequence.pin_id,
		sequence.start_time,
		sequence.start_range,
		sequence.end_time,
		sequence.end_range)
}
