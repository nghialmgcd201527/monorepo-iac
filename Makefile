.PHONY: build package changes deploy-core deploy-pipelines deploy destroy-core destroy-pipelines destroy

# define the name of the virtual environment directory
VENV := .venv
VENV_ACTIVATE := .venv/Scripts/activate

# default target, when make is executed without arguments: install virtualenv and project dependencies 
all: install

# Create virtualenv and install dependencies
install:
	@( \
		python -m venv $(VENV); \
		source $(VENV_ACTIVATE); \
		pip install -r requirements.txt; \
	  \
	)

# Bootstraping the cdk
bootstrap:
ifeq ("$(account-id)","")
	@echo "Error: account-id parameter is mandatory\n"
	@exit 1
endif
ifeq ("$(region)","")
	@echo "Error: region parameter is mandatory\n"
	@exit 1
endif
	@( \
		source $(VENV_ACTIVATE); \
		cdk bootstrap aws://${account-id}/${region}; \
	  \
	)

# Deploy monorepo core stack
 :
# ifneq ("$(monorepo-name)","")
# 	$(eval params_monorepo := --parameters MonorepoName=$(monorepo-name))
# endif
# 	@( \
# 		source $(VENV_ACTIVATE); \
# 		echo cdk deploy VizerpserverlessStack ${params_monorepo}; \
# 		cdk deploy VizerpserverlessStack ${params_monorepo}; \
# 	  \
# 	)

ifneq ("$(monorepo-name)","")
	$(eval params_monorepo := --parameters MonorepoName=$(monorepo-name))
endif
	@( \
		source $(VENV_ACTIVATE); \
		echo cdk deploy VizerpserverlessStack ${params_monorepo}; \
		cdk deploy VizerpserverlessStack ${params_monorepo}; \
	  \
	)

deploy-shareservice :

ifneq ("$(monorepo-name)","")
	$(eval params_monorepo := --parameters MonorepoName=$(monorepo-name))
endif
	@( \
		source $(VENV_ACTIVATE); \
		echo cdk deploy SharedServiceStack ${params_monorepo} --context environment=dev; \
		cdk deploy SharedServiceStack ${params_monorepo} --context environment=dev; \
	  \
	)
# Diff pipelines stack
diff-pipelines:
	@( \
		source $(VENV_ACTIVATE); \
		cdk diff PipelinesStack; \
	   \
	)
# Deploy pipelines stack Dev
deploy-pipelines:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy PipelineSharedServiceStackDev --context environment=dev; \
	   \
	)

# Deploy iam stack
deploy-iam:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy IamStack --context environment=dev; \
	   \
	)	

# Deploy codebuild stack
deploy-codebuild:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy CodebuildSharedServiceStack --context environment=dev; \
	   \
	)	

# Deploy pipelines stack QA
deploy-pipelines-qa:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy PipelineSharedServiceStackQa --context environment=qa; \
	   \
	)


deploy-serverlessPipelines:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy ServerlessPipelineStack; \
	   \
	)

# Deploy both stacks
deploy: deploy-core deploy-pipelines

# Destroy MonoRepo core stack
destroy-core:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy VizerpserverlessStack; \
	   \
	)

# Destroy Pipelines stack
destroy-pipelines:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy PipelinesStack; \
	   \
	)

# Remove virtual env files
clean-files:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

# Destroy all
destroy: destroy-pipelines destroy-core clean-files