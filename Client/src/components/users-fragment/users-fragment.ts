/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')

import { User } from '../../model/user'
import { Model } from '../../frame'
import { AppState } from '../../AppState'
import { Constants } from '../../config'

class ViewModel {
	router: any
    userModel: Model<User>
    users: KnockoutObservableArray<User>
    appState: AppState

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

        this.router = appState.router

        this.userModel = appState.getModel(Constants.model.user)
        this.users = ko.observableArray([])

        this.userModel.addObserver({
            objectAdded: this.addUser,
            objectModified: this.modifyUser,
            objectRemoved: this.removeUser
        })

        let globThis = this
        this.userModel.findAll({
            relation: [],
            attributes: []
        }).then((users) => {
            this.users(users)
        }, (error) => {
            console.log("Error!")
            globThis.router.transitionTo('login', { 
                backRoute: globThis.router.state.path 
            })
        })
    }

    public addUser = (user: User) => {
        this.users.push(user)
    }

    public modifyUser = (user: User) => {
    	var oldUser = ko.utils.arrayFirst(this.users(), (testUser: User) => {
    		return testUser.id == user.id
    	})
    	if (!oldUser) {
    		throw "Updated user not found!"
    	} else {
    		oldUser.update(user)
    	}
    }

    public removeUser = (user: User) => {
        this.users.remove(user)
    }

    public pushRemove = (user: User) => {
        this.userModel.remove(user, {
            relation: [],
            attributes: []
        })
    }

    public pushAdd = (params) => {
        this.router.transitionTo('add-user')
    }

    public pushUser = (user: User, event) => {
        this.router.transitionTo('sequences', { userId: user.id })
    }
}

export = ViewModel