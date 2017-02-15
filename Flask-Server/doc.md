# Structure

- Project
	* server.py
	* rest_model_adapter.py
	* requirements.txt
	* Module 1
		+ __init__.py
		+ dao.py (Data access objects) (merge with schema?)
		+ schema.py (Schema to marschall data) (JSON <-> dao)
		+ resources.py (custom resources) (if rest_model_adapter is not sufficient)
		+ ...
	* Module 2
		+ ...
	* ...