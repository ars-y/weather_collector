define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help: ## display available commands
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)

mkmgtrs: ## make migrations
mkmgtrs:
	alembic revision --autogenerate -m 'init_tables'

migrate: ## migrate
migrate:
	alembic upgrade head

clean: ## clean pycache
clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf