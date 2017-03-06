/// <reference path="./../typings/main.d.ts" />

export function routes(route) {
	route('login', { page: 'login-page', stack: false })
    route('/', { page: 'main-page', stack: false }, function() {
        route('pins', { page: 'pins-fragment', stack: true }, function() {
            route('add-pin', { path: '/pin/add', page: 'add-pin-fragment', stack: true })
            route('sequences', { path: '/pins/:pinId', page: 'sequences-fragment', stack: true }, function() {
                route('add-sequence', { path: '/pins/:pinId/add', page: 'add-sequence-fragment', stack: true })
            })
        })
    })
}
