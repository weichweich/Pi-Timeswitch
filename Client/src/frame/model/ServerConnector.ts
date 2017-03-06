/// <reference path="./../../../typings/main.d.ts" />

import { Constants } from '../../config'
let JsonApi: any = require('devour-client')
let jsonApi = new JsonApi({ apiUrl: Constants.backendURL })

import { Identifiable } from './Interfaces'

export interface Relation {
	type: string
	id: number
}

export type Parser<E> = {
	jsonToObject: (json: any) => E;
	objectToJson: (obj: E) => any;
}

export class ServerConnector<E extends Identifiable> {
	type: string
	jsonApi: any
	jsonToObject: (json: any) => any
	objectToJson: (obj: any) => any

	constructor(type: string, definition: {}, options: {}, parser: Parser<E>) {
		jsonApi.define(type, definition, options)
		this.jsonToObject = parser.jsonToObject
		this.objectToJson = parser.objectToJson
		this.type = type
	}

	public setJWTToken(token: string) {
		jsonApi.headers['auth'] = token
	}

	public getAll(relations: Relation[]) {
		for (let relation of relations) {
			jsonApi.one(relation.type, relation.id)
		}
		let obj = jsonApi.all(this.type).get()
			.then((data: any) => {
				let objects: E[] = []
				if (data != null) {
					objects = data.map(this.jsonToObject)
				}
				return objects
			}, this.error)
		return obj
		
	}

	public getOne(id: number) {
		return jsonApi.find(this.type, id)
			.then(this.jsonToObject, this.error)
	}

	public update(object: E, relations: Relation[]) {
		for (let relation of relations) {
			jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return jsonApi.one(this.type, object.id).patch(objJson)
			.then(this.jsonToObject, this.error)
	}

	public create(object: E, relations: Relation[]) {
		for (let relation of relations) {
			jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return jsonApi.all(this.type)
						.post(objJson)
						.then(this.jsonToObject, this.error)
	}

	public remove(object: E, relations: Relation[]) {
		for (let relation of relations) {
			jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return jsonApi.one(this.type, object.id).destroy(objJson)
			.then((json: any) => {
				return object
			}, this.error)
	}

	public error(data: any) {
		throw data
	} 
}