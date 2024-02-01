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

mv input/docs/kubernetes-reference/skupper.md input/docs/kubernetes-reference/index.md
mv input/docs/podman-reference/skupper.md input/docs/podman-reference/index.md


rm input/docs/kubernetes-reference/*.1
rm input/docs/podman-reference/*.1


./plano render --force