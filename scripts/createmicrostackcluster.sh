 #!/bin/bash
 sudo snap install microstack --classic --edge
 sudo microstack init --auto --control
 microstack.openstack endpoint list
 sudo cat /var/snap/microstack/common/etc/microstack.rc

 microstack.openstack server create \
--flavor m1.small \
--image "cirros" \
--network external \
my-first-instance