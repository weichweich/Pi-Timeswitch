/// <reference path="./../../../typings/main.d.ts" />

import { Identifiable } from './Interfaces'


export class Cache<E extends Identifiable> {
	cache: {[id: number]: E}

	constructor() {
		this.cache = {}
	}

	public storeAll = (objArray: [E]) => {
		for (let obj of objArray) {
			this.cache[obj.id] = obj
		}
	}

	public retrieveAll = () => {
		let objArray: E[] = []
		for (let key in this.cache) {
			objArray.push(this.cache[key])
		}
		return objArray
	}

	public retrieve = (id: number): E => {
		return this.cache[id]
	}

	public remove = (obj: E) => {
		delete this.cache[obj.id]
	}

	public store = (obj: E): E => {
		let old = this.cache[obj.id]
		this.cache[obj.id] = obj
		return old
	}
}