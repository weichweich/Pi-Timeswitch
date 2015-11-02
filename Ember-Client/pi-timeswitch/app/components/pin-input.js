import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'tr',
    actions: {
        addPin(value) {
            
            var name = this.get('name');
            var id = this.get('id');

            if (!isNaN(id) && name) {
                this.sendAction('action', id, name);
                this.set('name', '');
                this.set('id', '');
            }
        }
    }
});
