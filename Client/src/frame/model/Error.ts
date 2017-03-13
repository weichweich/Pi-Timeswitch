/// <reference path="./../../../typings/main.d.ts" />

export interface ErrorDescriptor {
	title: string
	code: number
	status: number
	detail: string
}

export class AuthenticationError extends Error {
    public name = "AuthenticationError";
    constructor (public message: string) {
        super(message);
    }
}

export class ValidationError extends Error {
    public name = "AuthenticationError";
    constructor (public message: string) {
        super(message);
    }
}