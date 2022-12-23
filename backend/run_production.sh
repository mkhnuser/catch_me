docker image build . -t mkhn/catch_me_production --target production
docker image prune -f
docker container run -p 8080:8080 -d --rm --name catch_me_production mkhn/catch_me_production
