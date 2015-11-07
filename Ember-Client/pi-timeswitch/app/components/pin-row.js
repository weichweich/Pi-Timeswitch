import Ember from 'ember';
import Constants from 'pi-timeswitch/constants';


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
            let pin = this.get(Constants.pinTag);

            if (Ember.get(pin, 'name') === "") {

            } else {
                this.sendAction('updatePinName', this.get(Constants.pinTag));
                this.set('editing', false);
            }
        },
        deletePin() {
            let pin = this.get('pin');
            this.sendAction('deletePin', pin);
        },
        focusOutInput() {
            this.set('editing', false);
        }
    }
});
