var ko = require('knockout'),
  template = require('./main-page.html');

var viewModel = function(params) {
    var self = this;
    self.model = params.model.model;
    self.store = params.model.store;

    self.title = ko.observable('Overview');
    self.pins = ko.observableArray([{
            pin_id: 1,
            number: 1,
            name: 'Blub',
            sequences: []
        },{
            pin_id: 2,
            number: 2,
            name: 'Blab',
            sequences: []
        },{
            pin_id: 3,
            number: 3,
            name: 'Bleb',
            sequences: []
        },{
            pin_id: 4,
            number: 4,
            name: 'Blib',
            sequences: []
        }]);

    self.model.pullAll('pins', function() {
        self.pins.removeAll();
        var newPins = self.store.findAll('pins');
        self.pins(newPins);
    })
    return self;
};

module.exports = {
  viewModel: viewModel,
  template: template
};