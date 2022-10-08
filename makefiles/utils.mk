f=""

.PHONY find:
find:
	find / -path */${f} 2> /dev/null
