import Ember from 'ember';

export default Ember.Route.extend({  
    model(params) {
        return Ember.RSVP.hash({
            pin: this.store.findRecord('pin', params.pin_id),
            sequences: this.store.findAll('sequence')
        });
    },
    actions: {
        createSequence(startTime, startRange, endTime, endRange) {

            this.store.createRecord('sequence', {
                startTime: startTime,
                startRange: startRange,
                endTime: endTime,
                endRange: endRange
            }).save();
        },
        updateSequence(sequence) {
            sequence.save();
        },
        deleteSequence(sequence) {
            sequence.destroyRecord();
        }

    }
});
