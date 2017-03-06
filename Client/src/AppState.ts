/// <reference path="./../typings/main.d.ts" />

import { Model } from "./frame"
import $ = require('jquery')

export class AppState {
	private models: { [id: string] : Model<any> }
	router: any

	constructor(router: any) {
		this.models = {}
		this.router = router
	}

	private setJWTToken(token: string) {
		for (var name in this.models) {
		    this.models[name].connection.setJWTToken(token)
		}
	}

	public unsetModel(name: string) {
		delete this.models[name]
	}

	public setModel(name: string, model: Model<any>) {
		this.models[name] = model
	}

	public getModel(name: string): Model<any> {
		return this.models[name]
	}

	// public isLoggedin(): boolean {
	// 	return false
	// }

	public logout() {
		location.reload()
	}

	public login(username: string, password: string) {
		let data = {
			'name': username,
			'password': password
		}
		let globThis = this
		return $.ajax({
			url: "api/login",
			type: "POST",
			data: JSON.stringify(data),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
		}).then(function(data) {
			let jsonObj = JSON.parse(data)
			if (jsonObj.token != null) {
				globThis.setJWTToken(jsonObj.token)
			} else {
				throw "login failed. JWT missing."
			}
		}, function(data) {
			throw data
		});
	}
}
