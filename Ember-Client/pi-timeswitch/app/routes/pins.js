import Ember from 'ember';

export default Ember.Route.extend({  
    model() {
        // var pins = [];
        // pins.push({
        //         state: 'on',
        //         id: 1,
        //         name: "Blub",
        //     });
        // pins.push({
        //         state: 'off',
        //         id: 2,
        //         name: "top",
        //     });
        // pins.push({
        //         state: 'on',
        //         id: 3,
        //         name: "hop",
        //     });
        // return pins;
        return this.store.findAll('pin');
    },
    actions: {
        createPin(id, name) {
            this.store.createRecord('pin', {
                state: 'off',
                id: id,
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
