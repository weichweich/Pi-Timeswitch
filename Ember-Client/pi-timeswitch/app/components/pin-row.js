import Ember from 'ember';

var PIN_TAG = 'pin';

export default Ember.Component.extend({
    tagName: 'tr',
    classNameBindings: ['editing'],
    editing: false,
    actions: {
        editPinName() {
            this.toggleProperty('editing');
            this.$().focus();
            
        },
        submitName() {
            let pin = this.get(PIN_TAG);

            if (Ember.get(pin, 'name') === "") {

            } else {
                this.sendAction('updatePinName', this.get(PIN_TAG));
                this.set('editing', false);
            }
        },
        deletePin() {
            let pin = this.get(PIN_TAG);
            this.sendAction('deletePin', pin);
        },
        focusOutInput() {
            this.set('editing', false);
        }
    }
});
