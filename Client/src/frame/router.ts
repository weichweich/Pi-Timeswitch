/// <reference path="./../../typings/main.d.ts" />

let cherrytree: any = require('cherrytree/standalone')


// Init properties
let cherryRouter = new cherrytree()

// create transition to update the current route stack.
cherryRouter.use((transition) => {

    let { routes, params } = transition
    let nextRouteStack = []

    // if only one route matches the given path
    // draw also routes that should not stack
    if (routes.length == 1) {
        nextRouteStack.push({
            page: routes[0].options.page,
            vals: routes[0].params,
        })

    // if multiple routes match the current path
    // draw every route which stackes (stack == true)
    } else {
        // array of configurations for the next routes.
        for (let route of routes) {

            if (route.options.stack) {
                nextRouteStack.push({
                    // the component which should be displayed
                    page: route.options.page,
                    // the params for this component
                    vals: route.params,
                })
            }
        }
    }
    // return nextRouteStack for use in next 
    return nextRouteStack
})


export let router = cherryRouter

export function startRouter() {
    cherryRouter.listen()
}