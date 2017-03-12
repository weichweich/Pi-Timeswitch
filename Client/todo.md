#Client todo

- improve UI
	* Modify Data:
		+ modify pin (name, state)
		+ modify sequence
		+ close sequence page if corresponding pin is deleted [implemented]
		+ input validation
		+ bind keys to buttons
	* Improved data handling
		+ client side caching (store data in a cache, so the model has to load it only once)
		+ all ViewModels should use the same KoObservables
		+ be prepared for server side updates
- Login/Logout
	* authentication [implemented]
	* delete all stored data on logout
- Overview Page
- typings
	* type for cherrytree router
	* type for ViewModel constructor param

- BUGS:
    * deleting newly created sequences raises 404 [implemented]
