var ko = require('knockout'),
    router = require('./router.js'),
    model = require('./model.js');

ko.components.register('main-page', require('./components/main-page/main-page.js'));
ko.components.register('pins-page', require('./components/pins-page/pins-page.js'));
ko.components.register('sequences-page', require('./components/sequences-page/sequences-page.js'));

// apply the view-model using KnockoutJS as normal
ko.applyBindings({ route: router.currentRoute, model: model });
