aws cloudformation deploy \
    --stack-name CommandLambda \
    --template-file CFTemplate.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
	