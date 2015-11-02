import Ember from 'ember';

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
            let pin = this.get('aPin');
            Ember.Logger.debug(pin);
            if (Ember.get(pin, 'name') === "") {

            } else {
                this.sendAction('updatePinName', this.get('pin'));
                this.set('editing', false);
            }
        },
        deletePin() {
            let pin = this.get('aPin');
            this.sendAction('deletePin', pin);
        },
        focusOutInput() {
            this.set('editing', false);
        }
    }
});
