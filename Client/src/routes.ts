/// <reference path="./../typings/main.d.ts" />

export function routes(route) {
	route('login', { page: 'login-page', stack: false })
    route('/', { page: 'main-page', stack: false })
    route('pins', { page: 'pins-fragment', stack: true }, function() {
        route('add-pin', { path: 'add', page: 'add-pin-fragment', stack: true })
        route('sequences', { path: 'pin/:pinId', page: 'sequences-fragment', stack: true }, function() {
            route('add-sequence', { path: '/pins/pin/:pinId/add', page: 'add-sequence-fragment', stack: true })
        })
    })
    route('users', { page: 'users-fragment', stack: true }, function() {
        route('add-user', { path: 'add', page: 'add-user-fragment', stack: true })
        route('user', { path: 'user/:userId', page: 'user-fragment', stack: true })
    })
}
