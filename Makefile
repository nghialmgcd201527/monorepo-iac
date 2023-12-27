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

# Deploy monorepo viz erp serverless stack
deploy-vizerpserverles :

ifneq ("$(monorepo-name)","")
	$(eval params_monorepo := --parameters MonorepoName=$(monorepo-name))
endif
	@( \
		source $(VENV_ACTIVATE); \
		echo cdk deploy VizerpserverlessStack ${params_monorepo} --context environment=dev; \
		cdk deploy VizerpserverlessStack ${params_monorepo} --context environment=dev; \
	  \
	)

# Diff monorepo viz erp serverless stack
diff-vizerpserverles :

ifneq ("$(monorepo-name)","")
	$(eval params_monorepo := --parameters MonorepoName=$(monorepo-name))
endif
	@( \
		source $(VENV_ACTIVATE); \
		echo cdk diff VizerpserverlessStack ${params_monorepo} --context environment=dev; \
		cdk diff VizerpserverlessStack ${params_monorepo} --context environment=dev; \
	  \
	)

# Deploy monorepo share service stack
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

# Deploy iam stack
deploy-iam:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy IamStack --context environment=dev; \
	   \
	)	

# Deploy codebuild share service repo
deploy-codebuild-shareservice:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy CodebuildSharedServiceStack --context environment=dev; \
	   \
	)	

# Deploy codebuild share service repo
deploy-codebuild-vizerpserverles:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy CodebuildVizErpServerlessServiceStack --context environment=dev; \
	   \
	)	
# Deploy pipelines stack Dev
deploy-pipelines-shareservice-dev:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy PipelineSharedServiceStackDev --context environment=dev; \
	   \
	)

# Deploy pipelines shared service qa
deploy-pipelines-shareservice-qa:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy PipelineSharedServiceStackQa --context environment=qa; \
	   \
	)

# Deploy pipelines viz erp serverles Dev
deploy-pipelines-vizerpserverles-dev:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy PipelineVizErpServerlessServiceStackDev --context environment=dev; \
	   \
	)

# Deploy pipelines viz erp serverles  qa
deploy-pipelines-vizerpserverles-qa:
	@( \
		source $(VENV_ACTIVATE); \
		cdk deploy PipelineVizErpServerlessServiceStackQa --context environment=qa; \
	   \
	)

# Deploy all for dev
deploy-dev: deploy-shareservice deploy-iam deploy-codebuild-shareservice deploy-codebuild-vizerpserverles deploy-pipelines-shareservice-dev deploy-pipelines-vizerpserverles-dev

# Deploy all for qa
deploy-qa: deploy-pipelines-shareservice-qa deploy-pipelines-vizerpserverles-qa

# Diff pipelines stack
diff-pipelines:
	@( \
		source $(VENV_ACTIVATE); \
		cdk diff PipelinesStack; \
	   \
	)
# Destroy vizerpserverles stack
destroy-vizerpserverles:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy VizerpserverlessStack --context environment=dev;; \
	   \
	)

# Destroy vizerpserverles stack
destroy-shareservice:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy SharedServiceStack --context environment=dev;; \
	   \
	)	

# Destroy iam stack
destroy-iam:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy IamStack --context environment=dev; \
	   \
	)

# Destroy codebuild share service repo
destroy-codebuild-shareservice:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy CodebuildSharedServiceStack --context environment=dev; \
	   \
	)	

# Destroy codebuild share service repo
destroy-codebuild-vizerpserverles:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy CodebuildVizErpServerlessServiceStack --context environment=dev; \
	   \
	)	

# Destroy pipelines stack Dev
destroy-pipelines-shareservice-dev:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy PipelineSharedServiceStackDev --context environment=dev; \
	   \
	)

# Destroy pipelines shared service qa
destroy-pipelines-shareservice-qa:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy PipelineSharedServiceStackQa --context environment=qa; \
	   \
	)


# Destroy pipelines viz erp serverles Dev
destroy-pipelines-vizerpserverles-dev:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy PipelineVizErpServerlessServiceStackDev --context environment=dev; \
	   \
	)

# Destroy pipelines viz erp serverles  qa
destroy-pipelines-vizerpserverles-qa:
	@( \
		source $(VENV_ACTIVATE); \
		cdk destroy PipelineVizErpServerlessServiceStackQa --context environment=qa; \
	   \
	)

# Destroy all for dev
destroy-dev: destroy-shareservice destroy-iam destroy-codebuild-shareservice destroy-codebuild-vizerpserverles destroy-pipelines-shareservice-dev destroy-pipelines-vizerpserverles-dev

# Destroy all for qa
destroy-qa: destroy-pipelines-shareservice-qa destroy-pipelines-vizerpserverles-qa

# Remove virtual env files
clean-files:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

# Destroy all
destroy: destroy-shareservice destroy-iam destroy-codebuild-shareservice destroy-codebuild-vizerpserverles destroy-pipelines-shareservice-dev destroy-pipelines-vizerpserverles-dev destroy-pipelines-shareservice-qa destroy-pipelines-vizerpserverles-qa clean-files