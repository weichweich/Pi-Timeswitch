/// <reference path="./../typings/main.d.ts" />

let _ = require('lodash')
import ko = require('knockout')
import { router, startRouter } from './frame/router'
import { routes } from "./routes"
import { AppState } from "./AppState"

export * from "./frame/router"
export * from "./frame/model/model"
export * from "./frame/model/Interfaces"

export function startApp() {
	let appState = new AppState(router)
	
	// observable array of current displayed routes
	let currentRouteStack = ko.observableArray([])
	
	// routes are extended with global obejcts and route specific properties:
	// router, view state, application state
	router.use(function(transition, nextRouteStack) {
		// update the currentRouteStack to macht the nextRouteStack
		let remove_count = currentRouteStack().length - nextRouteStack.length
		if (remove_count > 0) {
			currentRouteStack.splice(nextRouteStack.length, remove_count)
		}
	
		for (var _i = 0; _i < nextRouteStack.length; _i++) {
			let newRoute = {
				viewState: {
					index: _i,
					route: nextRouteStack[_i]
				},
				appState: appState
			} 
	
			if (currentRouteStack().length <= _i) {
				// current route stack is shorter 
				currentRouteStack.push(newRoute)
	
			} else if (!_.isEqual(newRoute, currentRouteStack()[_i])) {
				// if routes are not equal, replace with new one
				currentRouteStack()[_i] = newRoute
	
				// remove all routes after the current item on current stack
				// stack: [0, ..., _i, ... remove ...]
				if (currentRouteStack().length > _i) {
					let remove_count = currentRouteStack().length -_i -1
					currentRouteStack.splice(_i, remove_count)
				}
			}
		}
	})
	
	router.map(routes)
	
	startRouter()

	// ************** Set Root ViewModel **************
	ko.applyBindings({ 
		routeStack: currentRouteStack, 
		router: router
	});

	return appState
}
