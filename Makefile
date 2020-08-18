# Also needs to be updated in galaxy.yml
VERSION = 1.0.0

clean:
	rm -f community-kubernetes-${VERSION}.tar.gz
	rm -rf ansible_collections

build: clean
	ansible-galaxy collection build

release: build
	ansible-galaxy collection publish community-kubernetes-${VERSION}.tar.gz

install: build
	ansible-galaxy collection install -p ansible_collections community-kubernetes-${VERSION}.tar.gz

test-sanity:
	ansible-test sanity -v --docker --color $(TEST_ARGS)

test-integration:
	ansible-test integration --docker -v --color $(TEST_ARGS)

test-molecule:
	ansible-test integration --docker -v --color $(TEST_ARGS)

downstream-test-sanity: 
	./utils/downstream.sh -s

downstream-test-integration: 
	./utils/downstream.sh -i

downstream-test-molecule: 
	./utils/downstream.sh -m

downstream-build: 
	./utils/downstream.sh -b

downstream-release:
	./utils/downstream.sh -r
