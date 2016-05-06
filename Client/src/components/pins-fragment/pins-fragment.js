var ko = require('knockout'),
  template = require('./pins-fragment.html');

var viewModel = function(params) {
    var self = this;
    

    self.model = params.model.model;
    self.store = params.model.store;

    self.pins = ko.observableArray([]);
    self.fragment = ko.observable();
 
    self.model.pullAll('pins', function() {
        self.pins.removeAll();
        var newPins = self.store.findAll('pins');
        ko.utils.arrayForEach(newPins, function(pin) {
            self.pins.push(pin);
        });
    });

    self.removePin = function(params) {
        console.log('remove!');
        // console.log(params);
    };

    self.pinClicked = function(params) {
        console.log('clicked!');
        // console.log(params);
    };

    self.showPinAdd = function(params) {
        console.log('add!');
    }
};

module.exports = {
  viewModel: viewModel,
  template: template
};