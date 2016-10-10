# pyVagrantDemo
Vagrant box used for tutorials and demos found at https://medium.com/@michal.frystacky


## Quick Start
[Get started with vagrant](https://www.vagrantup.com/docs/getting-started/).

If your box is already setup:
Within the project's vagrant folder:
```
vagrant up
vagrant ssh  
```
In VM
``` bash
source /vagrant/restaurantExample/virtualenv/bin/activate
cd /vagrant/restaurantExample/
make -f Makefile
python generate_data.py
python restaurant_server.py
```
