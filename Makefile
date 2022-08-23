
reset:
# removing json and pickle files
	find -name "*.json" | xargs rm
	find -name "*.pickle" | xargs rm
