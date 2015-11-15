import Ember from 'ember';

export default Ember.Route.extend({
    model(params) {
      return this.store.findRecord('pin', params.pin_id);
    },
    actions: {
        createSequence(startTime, startRange, endTime, endRange, pin) {

            var sequence = this.store.createRecord('sequence', {
                startTime: startTime,
                startRange: startRange,
                endTime: endTime,
                endRange: endRange,
            });
            sequence.set('pin', pin);
            sequence.save();
        },
        updateSequence(sequence) {
            sequence.save();
        },
        deleteSequence(sequence) {
            sequence.destroyRecord();
        },
        error(error, transition) {
           if (error && error.status === 404) {
             return this.transitionTo('pins');
           }
           return this.transitionTo('pins');
         }
    }
});
