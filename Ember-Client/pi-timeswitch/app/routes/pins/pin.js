import Ember from 'ember';

export default Ember.Route.extend({  
    model() {
        let pin = [
            {
                "fromRange": "12:00", 
                "fromTm": "12:00", 
                "id": 1, 
                "pin": 1, 
                "toRange": "12:00", 
                "toTm": "12:00"
            }, 
            {
                "fromRange": "12:00", 
                "fromTm": "12:00", 
                "id": 2, 
                "pin": 2, 
                "toRange": "12:00", 
                "toTm": "12:00"
            }, 
            {
                "fromRange": "12:00", 
                "fromTm": "12:00", 
                "id": 3, 
                "pin": 3, 
                "toRange": "12:00", 
                "toTm": "12:00"
            }
        ];
        return pin;
        // return this.store.findAll('pin');
    }
});
