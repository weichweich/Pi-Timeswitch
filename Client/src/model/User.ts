/// <reference path="./../../typings/main.d.ts" />

import ko = require('knockout')

import { Identifiable } from '../frame'

export let definition = {
	name: '',
	privilege: '',
	password: '',
	email: ''
}

export let parser = {
	jsonToObject: jsonToUser,
	objectToJson: userToJson
}

export interface PinJson {
	id: number

	name: string
	privilege: string
	password: string
	email: string
}

export function jsonToUser(json: any): User {
	let user = new User(json.id, json.name, json.privilege, json.email)
	if (json.password != null) {
		user.password(json.password)
	}
	return user
}

export function userToJson(user: User) {
	return {
		id: user.id,
		username: ko.utils.unwrapObservable(user.name),
		privilege: ko.utils.unwrapObservable(user.privilege),
		email: ko.utils.unwrapObservable(user.email),
		password: ko.utils.unwrapObservable(user.password),
	}
}

export class User {
	id: number

	name: KnockoutObservable<string>
	password: KnockoutObservable<string>
	email: KnockoutObservable<string>
	privilege: KnockoutObservable<string>

	constructor(anID: number, aName: string, aPrivilege: string, anEmail: string) {
		this.id = anID
		this.name = ko.observable(aName)
		this.password = ko.observable('')
		this.email = ko.observable(anEmail)
		this.privilege = ko.observable(aPrivilege)
	}

	public update(user: User) {
		if (this.id != user.id) {
			throw "Updating user with diffrent user!"
		}
		this.name(user.name())
		this.email(user.email())
		this.password(user.password())
		this.privilege(user.privilege())
	}
}
