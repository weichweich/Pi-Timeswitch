var ko = require('knockout'),
    crossroads = require('crossroads'),
    hasher = require('hasher');

function Router(config) {
    var self = this
    self.currentRouteStack = ko.observableArray();
    self.nextRouteStack = [];

    ko.utils.arrayForEach(config.routes, function (routeConfig) {
        var route = crossroads.addRoute(routeConfig.url, function (requestParams) {
            self.nextRouteStack.push(ko.utils.extend(requestParams, routeConfig.params));
        }, routeConfig.prio);
        route.greedy = routeConfig.greedy;
    });

    /* DEBUG */
    // crossroads.routed.add(function(request, data) {
    //     console.log(request);
    //     console.log(data.route +' - '+ data.params +' - '+ data.isFirst);
    // });

    function parseHash(newHash, oldHash) {
        crossroads.parse(newHash);

        self.currentRouteStack(self.nextRouteStack);
        self.nextRouteStack = [];
    }

    function changeHash(newHash, oldHash) {
        var route = newHash;
        crossroads.parse(newHash);

        self.currentRouteStack(self.nextRouteStack);
        console.log(self.nextRouteStack);
        self.nextRouteStack = [];
    }
    crossroads.greedyEnabled = true;
    crossroads.normalizeFn = crossroads.NORM_AS_OBJECT;

    hasher.initialized.add(parseHash);
    hasher.changed.add(changeHash);
    hasher.init();
}

module.exports = new Router({
    routes: [
        { greedy: false, prio: 2, url: '', params: { page: 'main-page' } },
        { greedy: true,  prio: 2, url: '/pins/:add:', params: { page: 'pins-fragment' } },
        { greedy: true,  prio: 1, url: '/pins/add', params: { page: 'add-pin-fragment' } },
        // { greedy: true,  prio: 2, url: '/pin/{id}', params: { page: 'sequences-fragment' } },
    ]
});