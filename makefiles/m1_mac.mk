.PHONY: up_m1
up_m1:
	docker-compose -f docker-compose-for-m1-mac.yml up


.PHONY: build_m1
build_m1:
	docker-compose -f docker-compose-for-m1-mac.yml build
