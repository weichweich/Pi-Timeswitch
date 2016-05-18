/// <reference path="./../../typings/main.d.ts" />

import ko = require('knockout')

export interface SequenceJson {
	id: number

	start_time: string
	start_range: string

	end_time: string
	end_range: string
}

export class Sequence  {
	id: number

	start_time: KnockoutObservable<string>
	start_range: KnockoutObservable<string>

	end_time: KnockoutObservable<string>
	end_range: KnockoutObservable<string>

	constructor(anID: number, aStart_time: string, aStart_range: string, anEnd_time: string, anEnd_range: string) {
		this.id = anID

		this.start_time = ko.observable(aStart_time)
		this.start_range = ko.observable(aStart_range)

		this.end_time = ko.observable(anEnd_time)
		this.end_range = ko.observable(anEnd_range)
	}
}
