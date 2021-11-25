git add -A
echo "What is your commit message"
read msg
git commit -m "$msg"
git push origin master
docker build -t cscraper .
#docker push eugenebrod/cscraper
gcloud builds submit --tag gcr.io/cscraper/cscraper .
