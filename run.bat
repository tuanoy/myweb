docker image build -t myweb .
docker image tag myweb localhost:8080/asnpahp/myweb
docker image push localhost:8080/asnpahp/myweb 
kubectl apply -f ./kube-myweb/deployment.yaml
kubectl apply -f ./kube-myweb/service-nodeport.yaml