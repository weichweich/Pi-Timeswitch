var ko = require('knockout'),
  template = require('./pins-page.html');

var viewModel = function(params) {
    var self = this;
    
    self.model = params.model.model;
    self.store = params.model.store;
    
    self.pins = ko.observableArray([]);

    self.model.pullAll('pins', function() {
        self.pins.removeAll();
        var newPins = self.store.findAll('pins');
        ko.utils.arrayForEach(newPins, function(pin) {
            self.pins.push(pin);
        });
    });

    self.removePin = function() {

    };

    self.pinClicked = function() {
        
    };
};

module.exports = {
  viewModel: viewModel,
  template: template
};