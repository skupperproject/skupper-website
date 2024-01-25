cd input/docs
rm -r kubernetes-reference
rm -r podman-reference
skupper --platform kubernetes  man
mv docs.out kubernetes-reference
skupper --platform podman  man
mv docs.out podman-reference
cd ../..

python ./python/process-man.py input/docs/kubernetes-reference
python ./python/process-man.py input/docs/podman-reference

rm input/docs/kubernetes-reference/*.1
rm input/docs/podman-reference/*.1


./plano render --force