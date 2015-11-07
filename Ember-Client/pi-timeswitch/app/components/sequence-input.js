import Ember from 'ember';
import Constants from 'pi-timeswitch/constants';

function isAbsTime(time) {
    return Constants.absTimeRegex.test(time);
}
function isRelTime(time) {
    if (/^([0-9]+)$/.test(time)) {
        var num = Number(time);
        return (0 <= num) && (num <= 24*60);
    }
    return false;
}

export default Ember.Component.extend({
    tagName: 'tr',
    actions: {
        addSequence() {
            // get values
            var startTime = this.get(Constants.startTimeTag);
            var startRange = this.get(Constants.startRangeTag);
            var endTime = this.get(Constants.endTimeTag);
            var endRange = this.get(Constants.endRangeTag);
            var pinId = this.get('pin').get('pinNum');

            var valideData = startTime && startRange && endTime && endRange;

            if (valideData) {
                valideData &= (isAbsTime(startTime) && isRelTime(endTime))
                            || (isAbsTime(endTime) && isRelTime(startTime))
                            || (isAbsTime(endTime) && isAbsTime(startTime));
                valideData &= isRelTime(startRange);
                valideData &= isRelTime(endRange);
            }

            if (valideData) {
                this.sendAction('action', startTime, startRange, endTime,
                endRange, pinId);

                // clear values
                this.set(Constants.startTimeTag, '');
                this.set(Constants.startRangeTag, '');
                this.set(Constants.endTimeTag, '');
                this.set(Constants.endRangeTag, '');
            }
        }
    }
});
