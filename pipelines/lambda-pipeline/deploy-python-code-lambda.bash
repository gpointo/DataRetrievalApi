aws cloudformation deploy \
    --stack-name DataRetrievalLambdaDrop \
    --template-file lambdaPipeline.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
	