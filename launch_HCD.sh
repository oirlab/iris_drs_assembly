source configure_env.sh
cd pycsw/tests/
cd testSupport
sbt stage
test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf
