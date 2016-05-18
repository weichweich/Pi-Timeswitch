/// <reference path="./../typings/main.d.ts" />

import ko = require('knockout')
import crossroads = require('crossroads')
import hasher = require('hasher')

class Router {
    currentRouteStack :KnockoutObservableArray<any>
    nextRouteStack :any[]

    constructor(config: any) {
        this.currentRouteStack = ko.observableArray()
        this.nextRouteStack = []

        ko.utils.arrayForEach(config.routes, (routeConfig: any) => {
            let route = crossroads.addRoute(routeConfig.url, (requestParams) => {
                this.nextRouteStack.push(ko.utils.extend(requestParams, routeConfig.params));
            }, routeConfig.prio);
            route.greedy = routeConfig.greedy;
        });

        crossroads.greedyEnabled = true;
        crossroads.normalizeFn = crossroads.NORM_AS_OBJECT;
    
        hasher.initialized.add(this.parseHash, this);
        hasher.changed.add(this.changeHash, this);
        hasher.init();
    }

    parseHash(newHash, oldHash): void {
        crossroads.parse(newHash);

        this.currentRouteStack(this.nextRouteStack);
        this.nextRouteStack = [];
    }

    changeHash(newHash, oldHash): void {
        var route = newHash;
        crossroads.parse(newHash);

        this.currentRouteStack(this.nextRouteStack);
        console.log(this.nextRouteStack);
        this.nextRouteStack = [];
    }
}

let routes = {
    routes: [
        { greedy: false, prio: 2, url: '', params: { page: 'main-page' } },
        { greedy: true,  prio: 2, url: '/pins/:add:', params: { page: 'pins-fragment' } },
        { greedy: true,  prio: 1, url: '/pins/add', params: { page: 'add-pin-fragment' } },
        // { greedy: true,  prio: 2, url: '/pin/{id}', params: { page: 'sequences-fragment' } },
    ]
};

export = new Router(routes);