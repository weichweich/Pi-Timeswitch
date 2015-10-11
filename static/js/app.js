window.PiSchedule = Ember.Application.create({});

/* 
 * REST
 */

PiSchedule.ApplicationAdapter = DS.RESTAdapter.extend();
DS.RESTAdapter.reopen({
  namespace: 'api'
});

PiSchedule.Pin = DS.Model.extend({
	name: DS.attr('string'),
	schedules: DS.hasMany('schedule', {async: true})
});

PiSchedule.Schedule = DS.Model.extend({
	pin: DS.belongsTo('pin', {async: true}),
	fromTm: DS.attr('string'),
	fromRange: DS.attr('string'),
	toTm: DS.attr('string'),
	toRange: DS.attr('string')
})

/*
 * Router und Routes
 */

PiSchedule.Router.map(function() {
	this.resource('about');
	this.resource('pins', function() {
		this.resource('pin', { path: ':pin_id' });
	});
});

PiSchedule.PinsRoute = Ember.Route.extend({
	model: function() {
		return this.store.find('pin');
	}
});

PiSchedule.PinRoute = Ember.Route.extend({
	model: function(params) {
		return this.store.find('schedule');
	}
});

/* 
 * Controller
 */

PiSchedule.PinsController = Ember.ArrayController.extend({
	actions: {
		addPin: function () {
			var id = this.get('id');
			if (isNaN(id)) {
				this.set('isEditing', false);
			} else {
				this.set('isEditing', true);
				var name = this.get('name');
				
				var pin = this.store.createRecord('pin', {
					id: id,
					name: name
				});
				
				this.set('id', '');
				this.set('name', '');

				pin.save();
			}
		},
		pinChanged: function () {
			var id = this.get('id');
			if (isNaN(id)) {
				this.set('isEditing', false);
			} else {
				this.set('isEditing', true);
			}
		}
	},
	sortProperties: ['id'],
	sortAscending: true, // false = descending
	isValidPin: true,
});

PiSchedule.PinController = Ember.ObjectController.extend({
	isEditing: false,
	
	actions: {
		editPin: function() {
			this.set('isEditing', true);
		},
		acceptChanges: function() {
			this.set('isEditing', false);

			this.get('model').save();
		},
		removePin: function () {
			var pin = this.get('model');
			pin.deleteRecord();
			pin.save();
		},
		addTime: function () {
			var from = this.get('fromTm');
			var fromRange = this.get('fromRange');
			var to = this.get('toTm');
			var toRange = this.get('toRange');
			var pin = this.get('model');
			
			var schedule = this.store.createRecord('schedule' ,{
				fromTm: from,
				fromRange: fromRange,
				toTm: to,
				toRange: toRange,
				pin: pin
			});
				
			this.set('fromTm', '');
			this.set('fromRange', '');
			this.set('toTm', '');
			this.set('toRange', '');

			schedule.save();
		}
	},
	timeChanged: function () {
		var id = this.get('id');
		if (isNaN(id)) {
			this.set('isEditing', false);
		} else {
			this.set('isEditing', true);
		}
	}
});

PiSchedule.TimeController = Ember.ObjectController.extend({
	isEditing: false,
	
	actions: {
		editTime: function() {
			this.set('isEditing', true);
		},
		acceptChanges: function() {
			this.set('isEditing', false);
			this.get('model').save();
		},
		removeTime: function () {
			var time = this.get('model');
			time.deleteRecord();
			time.save();
		}
	}
});