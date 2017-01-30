/// <reference path="./../../typings/main.d.ts" />

import config = require('./../config')

var JsonApi = require('devour-client')

let jsonApi = new JsonApi({ apiUrl: config.backendURL })

import { Identifiable } from './Interfaces.ts'

export interface Relation {
	type: string
	id: number
}

export class ServerConnector<E extends Identifiable> {
	type: string

	jsonToObject: any
	objectToJson: any

	constructor(type: string, definition: {}, options: {}, parser: any) {
		jsonApi.define(type, definition, options)
		this.jsonToObject = parser.jsonToObject
		this.objectToJson = parser.objectToJson
		this.type = type
	}

	public getAll = (relations: Relation[]) => {
		let requenst = jsonApi
		for (let relation of relations) {
			requenst.one(relation.type, relation.id)
		}
		return requenst.all(this.type).get()
			.then((data: any[]) => {

				let objects: E[] = []
				for (let json of data) {
					objects.push(this.jsonToObject(json))
				}
				return objects
			}, (data) => { return data })
	}

	public getOne = (id: number) => {
		return jsonApi.find(this.type, id)
			.then(this.jsonToObject, this.error)
	}

	public update = (object: E, relations: Relation[]) => {
		let requenst = jsonApi
		for (let relation of relations) {
			requenst.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return requenst.one(this.type, object.id).patch(objJson)
			.then(this.jsonToObject, this.error)
	}

	public create = (object: E, relations: Relation[]) => {
		let requenst = jsonApi
		for (let relation of relations) {
			requenst.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return requenst.all(this.type).post(objJson)
					  .then(this.jsonToObject, this.error)
	}

	public remove = (object: E, relations: Relation[]) => {
		let requenst = jsonApi
		for (let relation of relations) {
			requenst.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return requenst.one(this.type, object.id).destroy(objJson)
			.then((json: any) => {
				return object
			}, this.error)
	}

	public error = (data: any) => {
		console.log('ServerConnection - Error: ', data)
	} 
}