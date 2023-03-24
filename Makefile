
reset:
# removing json and pickle files
	find -name "*.json" | xargs rm
	find -name "*.pickle" | xargs rm

restart:
# removing json and pickle files
	find -name "*.pickle" | xargs rm

reset_alerts:
	find -name "*.pickle" | xargs rm

	