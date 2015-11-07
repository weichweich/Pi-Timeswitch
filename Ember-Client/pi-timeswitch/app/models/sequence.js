import DS from 'ember-data';

export default DS.Model.extend({
    startTime: DS.attr('string'),
    startRange: DS.attr('string'),
    endTime: DS.attr('string'),
    endRange: DS.attr('string'),
    pinId: DS.attr('string')
});
