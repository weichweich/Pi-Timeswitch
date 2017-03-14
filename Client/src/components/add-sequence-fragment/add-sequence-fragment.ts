/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')
import { Pin } from '../../model/pin'
import { Sequence } from '../../model/Sequence'
import { Model, AppState } from '../../frame'
import { Constants } from '../../config'

class ViewModel {
    sequenceModel :Model<Sequence>
    state: KnockoutObservable<string>
    router: any
    appState: AppState

    start_time: KnockoutObservable<string>
    start_range: KnockoutObservable<string>
    
    end_time: KnockoutObservable<string>
    end_range: KnockoutObservable<string>

    pinId: number

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

        this.router = appState.router
        this.sequenceModel = appState.getModel(Constants.model.sequence)

        this.state = ko.observable('ready') // possible: ready, uploading 

        this.pinId = viewState.route.vals.pinId
        this.start_time = ko.observable('')
        this.start_range = ko.observable('')
        this.end_time = ko.observable('')
        this.end_range = ko.observable('')
    }

    public cancle = (params) => {
        // length of current route stack
        let length = this.router.state.routes.length
        // get the route bevor the current route
        let last_route = this.router.state.routes[length-2]
        this.router.transitionTo(last_route.name)
    }

    public addSequence = (params) => {
        if (this.state() !== 'ready') {
            return
        }

        this.stateUploading()

        let aStart_time = ko.utils.unwrapObservable(this.start_time)
        let aStart_range = ko.utils.unwrapObservable(this.start_range)
        let aEnd_time = ko.utils.unwrapObservable(this.end_time)
        let aEnd_range = ko.utils.unwrapObservable(this.end_range)

        let newSequence = new Sequence(-1, this.pinId, aStart_time,
            aStart_range, aEnd_time, aEnd_range)

        this.sequenceModel.create(newSequence, {
                relation: [{
                    type: 'pin',
                    id: this.pinId
                }],
                attributes: []
            }).then((respons) => {
                this.start_time('')
                this.start_range('')
                this.end_time('')
                this.end_range('')
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
