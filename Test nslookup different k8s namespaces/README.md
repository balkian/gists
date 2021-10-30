```
kubectl apply -f pruebans1.yml
kubectl apply -f pruebans2.yml
```

```
kubectl exec -ti $(kubectl get pods -n pruebans1 --no-headers -o custom-columns=":metadata.name")  -n pruebans1 -- nslookup pruebans2.pruebans2
```
