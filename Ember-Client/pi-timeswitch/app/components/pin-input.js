import Ember from 'ember';

function filterInt(value) {
    if(/^([0-9]+)$/.test(value)) {
        return Number(value);
    }
    return NaN;
}

export default Ember.Component.extend({
    tagName: 'tr',
    actions: {
        addPin() {
            var name = this.get('name');
            var pin_num = filterInt(this.get('pin_num'));

            if (!isNaN(pin_num) && name) {
                this.sendAction('action', pin_num, name);
                this.set('name', '');
                this.set('pin_num', '');
            }
        }
    }
});
