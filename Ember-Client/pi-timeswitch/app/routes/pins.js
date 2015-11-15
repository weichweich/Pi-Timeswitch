import Ember from 'ember';

export default Ember.Route.extend({
    model: function() {
        return this.store.findAll('pin');
    },
    actions: {
        createPin(pinNum, name) {
            this.store.createRecord('pin', {
                state: 0,
                pinNum: pinNum,
                id: pinNum,
                name: name
            }).save();
        },
        updatePinName(pin) {
            pin.save();
        },
        deletePin(pin) {
            pin.destroyRecord();
        }

    }
});
