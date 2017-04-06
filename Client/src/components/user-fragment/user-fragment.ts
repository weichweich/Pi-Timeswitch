/// <reference path="./../../../typings/main.d.ts" />

import ko = require('knockout')

import { User } from '../../model/user'
import { Model, AppState } from '../../frame'
import { Constants } from '../../config'

interface UserChanger {
    user: KnockoutObservable<User>
	checkNewPwd: KnockoutObservable<string>
    pwdErrors: KnockoutComputed<string[]>
    noError: KnockoutComputed<boolean>
}

class ViewModel {
	router: any
    userModel: Model<User>

    user: KnockoutObservable<User>
    userChanger: KnockoutObservable<UserChanger>

    appState: AppState
    index: number

	constructor(params) {
		let viewState = params.viewState
		let appState = params.appState

        this.router = appState.router
		this.index = viewState.index
		
		this.user = ko.observable(undefined)
		this.userChanger = ko.observable(undefined)

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
    	if (this.user().id == user.id) {
    		this.user().update(user)
    	}
    }

    public removeUser = (user: User) => {
    	if (this.user().id == user.id) {
        	let last_route = this.router.state.routes[this.index]
        	this.router.transitionTo(last_route.name)
    	}
    }

    public pushShowChange = (user: User) => {
        let globThis = this
    	this.userChanger(<UserChanger> {
            user: globThis.user,
    		checkNewPwd: ko.observable(""),
            pwdErrors: ko.computed(() => {
                    let errors = []
                    if (globThis.userChanger() != undefined) {
                        if (globThis.userChanger().user().password() == "") {
                            errors.push("The old password is missing!")
                        }
                        if (globThis.userChanger().user().newPassword() == "") {
                            errors.push("the new password is missing!")
                        } else if (globThis.userChanger().user().newPassword() !== globThis.userChanger().checkNewPwd()) {
                            errors.push("Passwords don't match!")
                        }
                    }
                    return errors
                }),
            noError: ko.computed(() => {
                    if (globThis.userChanger() != undefined 
                        && globThis.userChanger().pwdErrors().length == 0) {
                        return true
                    }
                    return false
                })
        })

    }

    public pushSave = (user: User) => {
        console.log("save!")
        this.userModel.update(this.userChanger().user()).then((data) => {
            this.userChanger(undefined)
        }, (error) => {
            console.log("User update failed. This error is unhanled.", error)
        })
    }

    public pushCancle = (user: User) => {
    	this.userChanger(undefined)
    }
}

export = ViewModel