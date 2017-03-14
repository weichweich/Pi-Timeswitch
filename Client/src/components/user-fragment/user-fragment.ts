/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')

import { User } from '../../model/user'
import { Model, AppState } from '../../frame'
import { Constants } from '../../config'

class ViewModel {
	router: any
    userModel: Model<User>
    user: KnockoutObservable<User>
    appState: AppState
    index: number

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

        this.router = appState.router
		this.index = viewState.index
		this.user = ko.observable(undefined)
        this.userModel = appState.getModel(Constants.model.user)
        this.userModel.addObserver({
            objectAdded: this.addUser,
            objectModified: this.modifyUser,
            objectRemoved: this.removeUser
        })

        let globThis = this
        this.userModel.findOne(viewState.route.vals.userId)
                      .then((user) => {
            this.user(user)
        }, (error) => {
            console.log("Error!")
            globThis.router.transitionTo('login', { 
                backRoute: globThis.router.state.path 
            })
        })
    }

    public addUser = (user: User) => {
    }

    public modifyUser = (user: User) => {
    	if (this.user.id == user.id) {
    		this.user().update(user)
    	}
    }

    public removeUser = (user: User) => {
    	if (this.user.id == user.id) {
        	let last_route = this.router.state.routes[this.index]
        	this.router.transitionTo(last_route.name)
    	}
    }
}

export = ViewModel