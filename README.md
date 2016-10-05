# pyVagrantDemo
Vagrant box used for tutorials and demos found at https://medium.com/@michal.frystacky


## Quick Start
If you setup the provisions for the vagrant VM very few steps are needed to get up and running.
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
