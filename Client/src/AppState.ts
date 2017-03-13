/// <reference path="./../typings/main.d.ts" />

import { Model, cookie } from "./frame"
import $ = require('jquery')

export class AppState {
	private models: { [id: string] : Model<any> }
	private token: string
	router: any
	static readonly JWT_IDENTIFIER = 'AppState.jwt'

	constructor(router: any) {
		this.models = {}
		this.router = router
		this.setToken(cookie.read(AppState.JWT_IDENTIFIER))
	}

	private setToken(token: string) {
		this.token = token
		for (var name in this.models) {
		    this.models[name].connection.setJWTToken(token)
		}
	}

	public unsetModel(name: string) {
		delete this.models[name]
	}

	public setModel(name: string, model: Model<any>) {
		this.models[name] = model
		this.models[name].connection.setJWTToken(this.token)
	}

	public getModel(name: string): Model<any> {
		return this.models[name]
	}

	// public isLoggedin(): boolean {
	// 	return false
	// }

	public logout() {
		cookie.remove(AppState.JWT_IDENTIFIER)
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
			if (data.token != null) {
				globThis.setToken(data.token)
				cookie.write(AppState.JWT_IDENTIFIER, data.token)
			} else {
				throw "login failed. JWT missing."
			}
		}, function(data) {
			throw data
		});
	}
}
