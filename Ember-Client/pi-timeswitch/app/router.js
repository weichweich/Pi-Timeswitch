import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
    location: config.locationType
});

Router.map(function() {
    this.route('about');
    this.route('pins', function() {
        this.route('pin', {path: ':pin_id'});
    });
});

export default Router;
