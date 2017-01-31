/// <reference path="../../../typings/main.d.ts" />

import ko = require('knockout')

import { Pin } from '../../model/pin.ts'
import { Sequence } from '../../model/sequence.ts'
import { Model } from '../../Model'
import router from '../../router.ts'

class ViewModel {
    router: any
    pinModel: Model<Pin>
    index: number

    title: KnockoutObservable<string>
    pins: KnockoutObservableArray<Pin>

    constructor(params) {
        this.router = params.router
        this.index = params.index
        this.pinModel = params.model.pin
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