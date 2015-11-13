import DS from 'ember-data';

export default DS.Model.extend({
    name: DS.attr('string'),
    state: DS.attr('string'),
    pinNum: DS.attr('string'),
    sequences: DS.hasMany('sequence', { async: true })
});
