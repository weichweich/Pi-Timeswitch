import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'tr',
    classNameBindings: ['editing'],
    editing: false,
    actions: {
        editSequence() {
            this.toggleProperty('editing');
            this.$().focus();
            
        },
        submitSequenceChange() {
            var startTime = this.get(Constants.startTimeTag);
            var startRange = this.get(Constants.startRangeTag);
            var endTime = this.get(Constants.endTimeTag);
            var endRange = this.get(Constants.endRangeTag);

            if (startTime && startRange && endTime && endRange) {

                this.sendAction('updateSequence', startTime, startRange, endTime, endRange);
                this.set('editing', false);
            }
        },
        deleteSequence() {
            let pin = this.get(PIN_TAG);
            this.sendAction('deletePin', pin);
        },
        focusOutInput() {
            this.set('editing', false);
        }
    }
});
