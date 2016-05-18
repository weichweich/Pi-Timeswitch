/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')
import { Pin } from '../../model/pin.ts'
import { Sequence } from '../../model/sequence.ts'
import { Model } from '../../Model'

class ViewModel {
    
    model :Model
    name :KnockoutObservable<string>
    number :KnockoutObservable<number>
    state: KnockoutObservable<string>

    constructor(params) {
        this.model = params.model
        this.name = ko.observable('')
        this.number = ko.observable(-1)
        this.state = ko.observable('ready') // possible: ready, uploading 
    }

    public cancle = (params) => {
        window.location.href = '#/pins'
    }

    public addPin = (params) => {
        if (this.state() !== 'ready') {
            return
        }

        this.stateUploading()

        let aName = ko.utils.unwrapObservable(this.name)
        let aNumber = ko.utils.unwrapObservable(this.number)

        this.model.createPin(new Pin(aNumber, aNumber, aName, 0, []))
                  .then((respons) => {
                        this.name('')
                        this.number(0)
                        this.stateReady()
                  })
    }

    public stateUploading = () => {
        this.state('uploading')
    }
    public stateReady = () => {
        this.state('ready')
    }
}

export = ViewModel
