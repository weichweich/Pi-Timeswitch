/// <reference path="../../../typings/main.d.ts" />

import { AppState } from '../../frame'
import { Constants } from '../../config'

class ViewModel {
    appState: AppState

	constructor(params) {
		// let viewState = params.viewState
		this.appState = params.appState
	}

    public pushLogout = () => {
    	this.appState.logout()
    	this.appState.router.transitionTo('login')
    }

    public pushLogo = () => {
    	this.appState.router.transitionTo('/')
    }
}

export = ViewModel
