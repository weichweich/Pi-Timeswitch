import Ember from 'ember';
import Constants from 'pi-timeswitch/constants';

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
            var sequence = this.get('sequence');

            if (startTime && startRange && endTime && endRange) {

                this.sendAction('updateSequence', startTime, startRange,
                    endTime, endRange, sequence.get('pinId'));
                this.set('editing', false);
            }
        },
        deleteSequence() {
            var sequence = this.get('sequence');
            if (sequence) {
                this.sendAction('deleteSequence', sequence);
            } else {
                Ember.Logger.error('Delete undefined sequence!');
            }
        },
        focusOutInput() {
            this.set('editing', false);
        }
    }
});
