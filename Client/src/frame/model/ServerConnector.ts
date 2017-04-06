/// <reference path="./../../../typings/main.d.ts" />

import { Constants } from '../../config'
let JsonApi: any = require('devour-client')
let jsonApi = new JsonApi({ apiUrl: Constants.backendURL })

import { Identifiable } from './Interfaces'
import { AuthenticationError, ErrorDescriptor } from './Error'

let errorMiddleware = {
	name: 'error-formatter',
	error: function (payload) {
		let errors: ErrorDescriptor[] = []
		for (let err of payload.data.errors) {
			errors.push(<ErrorDescriptor><any> err)
		}
		return errors
	}
}
jsonApi.replaceMiddleware('errors', errorMiddleware)

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
		return jsonApi.all(this.type).get()
			.then((data: any) => {
				let objects: E[] = []
				if (data != null) {
					objects = data.map(this.jsonToObject)
				}
				return objects
			}, this.error)		
	}

	public getOne(id: number) {
		return jsonApi.find(this.type, id)
			.then(this.jsonToObject, this.error)
	}

	public update(object: E, relations: Relation[] =[]) {
		for (let relation of relations) {
			jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return jsonApi.one(this.type, object.id).patch(objJson)
			.then(this.jsonToObject, this.error)
	}

	public create(object: E, relations: Relation[] =[]) {
		for (let relation of relations) {
			jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return jsonApi.all(this.type)
						.post(objJson)
						.then(this.jsonToObject, this.error)
	}

	public remove(object: E, relations: Relation[] =[]) {
		for (let relation of relations) {
			jsonApi.one(relation.type, relation.id)
		}
		let objJson = this.objectToJson(object)
		return jsonApi.one(this.type, object.id).destroy(objJson)
			.then((json: any) => {
				console.log("deleted", json)
				return object
			}, this.error)
	}

	public error(errors: ErrorDescriptor[]) {
		for (let err of errors) {
			if (err.code == 401) {
				throw new AuthenticationError(err.detail)
			}
		}
		throw errors
		
	} 
}