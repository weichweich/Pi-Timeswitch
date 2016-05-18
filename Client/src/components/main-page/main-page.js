/// <reference path="../../../typings/main.d.ts" />

var ko = require('knockout'),
  template = require('./main-page.html');

var viewModel = function(params) {
    var self = this;

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

    return self;
};

module.exports = {
  viewModel: viewModel,
  template: template
};