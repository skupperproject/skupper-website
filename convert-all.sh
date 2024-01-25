bash ./convert-adoc.sh cli/index.adoc cli/tokens.adoc cli/podman.adoc cli/native-security-options.adoc yaml/index.adoc operator/index.adoc console/index.adoc policy/index.adoc troubleshooting/index.adoc overview/connectivity.adoc overview/glossary.adoc overview/index.adoc overview/resources.adoc overview/routing.adoc overview/security.adoc

cp -r subrepos/skupper-docs/images/ input/docs/

# To process nested numbered lists
python python/nested-numbers.py input/docs/operator/

./plano render --force