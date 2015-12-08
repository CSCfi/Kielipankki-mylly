pouta-ansible-demo
==================

Simple Ansible demo to deploy a machine to Pouta

To use this demo you will need:
 - Ansible 2.0:
  http://docs.ansible.com/intro_installation.html
   (clone the git repo and use the devel branch)
 - OpenStack command line tools:
   http://docs.openstack.org/user-guide/content/install_clients.html
 - Access to pouta:
   https://research.csc.fi/pouta-access
 - Your Pouta openstack RC file:
   https://research.csc.fi/pouta-install-client
 - Shade: pip install shade
   http://docs.openstack.org/infra/shade/

Configuration:

You will need to get some information from your pouta account in order to run this demo. See the comments in demo.yml.

To launch the demo:

    ansible-playbook demo.yml
