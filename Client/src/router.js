var ko = require('knockout'),
    crossroads = require('crossroads'),
    hasher = require('hasher');

function Router(config) {
    var self = this
    self.currentRoute = ko.observable({});

    ko.utils.arrayForEach(config.routes, function (route) {
        crossroads.addRoute(route.url, function (requestParams) {
            self.currentRoute(ko.utils.extend(requestParams, route.params));
        });
    });
    
    /* DEBUG */
    // crossroads.routed.add(function(request, data) {
    //     console.log(request);
    //     console.log(data.route +' - '+ data.params +' - '+ data.isFirst);
    // });

    activateCrossroads();
}

function activateCrossroads() {
    function parseHash(newHash, oldHash)
    {
        crossroads.parse(newHash);
    }

    function changeHash(newHash, oldHash) {
        var route = newHash;

        crossroads.parse(newHash);
    }
    crossroads.normalizeFn = crossroads.NORM_AS_OBJECT;

    hasher.initialized.add(parseHash);
    hasher.changed.add(changeHash);
    hasher.init();
}

module.exports = new Router({
    routes: [
        { url: '', params: { page: 'main-page' } },
        { url: '/pins', params: { page: 'pins-page' } },
    ]
});