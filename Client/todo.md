#Client todo

- improve UI
	* modify pin name, state
	* modify sequence
	* close sequence page if corresponding pin is deleted [implemented]
	* input validation
	* bind keys to buttons
- Login/Logout
	* authentication
	* delete all stored data on logout
- Overview Page
- live updates from server
- typings
	* type for cherrytree router
	* type for ViewModel constructor param

- BUGS:
    * deleting newly created sequences raises 404
        + sequence.id is not updated
        + server creates id's
        + create ids on client side?