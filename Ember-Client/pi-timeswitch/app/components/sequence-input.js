import Ember from 'ember';
import Constants from 'pi-timeswitch/constants';

export default Ember.Component.extend({
    tagName: 'tr',
    actions: {
        addSequence() {
            // get values
            var startTime = this.get(Constants.startTimeTag);
            var startRange = this.get(Constants.startRangeTag);
            var endTime = this.get(Constants.endTimeTag);
            var endRange = this.get(Constants.endRangeTag);

            if (startTime && startRange && endTime && endRange) {
                this.sendAction('action', startTime, startRange, endTime, endRange);

                // clear values
                this.set(Constants.startTimeTag, '');
                this.set(Constants.startRangeTag, '');
                this.set(Constants.endTimeTag, '');
                this.set(Constants.endRangeTag, '');
            }
        }
    }
});
