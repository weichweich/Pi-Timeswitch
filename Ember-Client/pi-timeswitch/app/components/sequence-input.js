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
            var pin = this.get('pin');

            var valideData = false;

            if (startTime && startRange && endTime && endRange) {
                if (isAbsTime(endTime)) {
                    if (isAbsTime(startTime) || isRelTime(startTime)) {
                        valideData = true;
                    } else {
                        alert('Start time must be a valide time');
                    }
                } else if (isRelTime(endTime)) {
                    if (isAbsTime(startTime)) {
                        valideData = true;
                    } else {
                        alert('Start time must be a valide absolute time');
                    }
                } else {
                    alert('End time must be a valide time!');
                }
            } else {
                alert('A field is null!');
            }

            valideData &= isRelTime(startRange);
            valideData &= isRelTime(endRange);

            if (valideData) {

                this.sendAction('action', startTime, startRange, endTime,
                endRange, pin);

                // clear values
                this.set(Constants.startTimeTag, '');
                this.set(Constants.startRangeTag, '');
                this.set(Constants.endTimeTag, '');
                this.set(Constants.endRangeTag, '');
            }
        }
    }
});
