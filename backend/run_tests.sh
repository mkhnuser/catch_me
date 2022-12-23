docker image build . -t mkhn/catch_me_testing --target testing
docker image prune -f
docker container run -it --rm --name catch_me_testing mkhn/catch_me_testing
