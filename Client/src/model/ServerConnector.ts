/// <reference path="./../../typings/main.d.ts" />

import config = require('./../config')
let JsonApi: any = require('devour-client')

let errorMiddleware = {
  name: 'custom-error-handler',
  error: function (payload) {
  	console.log("mh", payload)
  	return 'error!!'
  }
}

import { Identifiable } from './Interfaces'

export interface Relation {
	type: string
	id: number
}

export class ServerConnector<E extends Identifiable> {
	type: string
	jsonApi: any
	jsonToObject: any
	objectToJson: any

	constructor(type: string, definition: {}, options: {}, parser: any) {
		this.jsonApi = new JsonApi({ apiUrl: config.backendURL })
		// this.jsonApi.replaceMiddleware('errors', errorMiddleware)

		this.jsonApi.define(type, definition, options)
		this.jsonToObject = parser.jsonToObject
		this.objectToJson = parser.objectToJson
		this.type = type
	}

	public setJWTToken = (token: string) => {
		this.jsonApi.headers['auth'] = token
	}

	public getAll = (relations: Relation[]) => {
		for (let relation of relations) {
			this.jsonApi.one(relation.type, relation.id)
		}
		return this.jsonApi.all(this.type).get()
			.then((data: any[]) => {

				let objects: E[] = []
				for (let json of data) {
					objects.push(this.jsonToObject(json))
				}
				return objects
			}, (data) => { return data })
	}

	public getOne = (id: number) => {
		return this.jsonApi.find(this.type, id)
			.then(this.jsonToObject, this.error)
	}

	public update = (object: E, relations: Relation[]) => {
		for (let relation of relations) {
			this.jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return this.jsonApi.one(this.type, object.id).patch(objJson)
			.then(this.jsonToObject, this.error)
	}

	public create = (object: E, relations: Relation[]) => {
		for (let relation of relations) {
			this.jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return this.jsonApi.all(this.type).post(objJson)
					  .then(this.jsonToObject, this.error)
	}

	public remove = (object: E, relations: Relation[]) => {
		for (let relation of relations) {
			this.jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return this.jsonApi.one(this.type, object.id).destroy(objJson)
			.then((json: any) => {
				return object
			}, this.error)
	}

	public error = (data: any) => {
		console.log('ServerConnection - Error: ', data)
	} 
}