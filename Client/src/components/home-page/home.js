import ko from 'knockout';
import homeTemplate from 'text!./home.html';

class HomeViewModel {
    constructor(route) {
        this.title = ko.observable('Overview');
        this.pins = ko.observableArray([{
            pin_id: 1,
            number: 1,
            name: 'Blub',
            sequences: []
        },{
            pin_id: 2,
            number: 2,
            name: 'Blab',
            sequences: []
        },{
            pin_id: 3,
            number: 3,
            name: 'Bleb',
            sequences: []
        },{
            pin_id: 4,
            number: 4,
            name: 'Blib',
            sequences: []
        }]);
    }
    
    doSomething() {
        this.message('You invoked doSomething() on the viewmodel.');
    }
}

export default { viewModel: HomeViewModel, template: homeTemplate };