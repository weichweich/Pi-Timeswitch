/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')
import { Pin } from '../../model/pin.ts'
import { Sequence } from '../../model/sequence.ts'
import { Model } from '../../Model'


class ViewModel {
    model: Model
    pins: KnockoutObservableArray<Pin>

    constructor (params) {
        this.model = params.model

        this.pins = this.model.pins
    }

    public removePin = (pin: Pin) => {
        this.model.deletePin(pin)
    }

    public pinClicked = (params) => {
        console.log('clicked!')
        // console.log(params)
        console.log(this.pins())
    }
}

export = ViewModel