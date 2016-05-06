var ko = require('knockout'),
	template = require('./add-pin-fragment.html')

var viewModel = function(params) {
	var self = this;
	self.fromTime = ko.observable();
	self.fromRange = ko.observable();
	self.endTime = ko.observable();
	self.endRange = ko.observable();
};

module.exports = {
  viewModel: viewModel,
  template: template
};