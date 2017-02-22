/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin'
import { Sequence } from '../../model/sequence'
import { Model } from '../../Model'
import router from '../../router'

class ViewModel {
    router: any
    pinModel: Model<Pin>
    index: number

    title: KnockoutObservable<string>
    pins: KnockoutObservableArray<Pin>

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

        this.router = appState.router
        this.index = viewState.index
        this.pinModel = appState.model.pin
        this.pins = ko.observableArray([])
        this.title = ko.observable('Overview!')

        this.pinModel.findAll({
            relation: [],
            attributes: []
        }).then((pins) => {
            this.pins(pins)
        })
    }
};

export = ViewModel