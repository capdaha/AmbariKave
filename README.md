AmbariKave
==========

This repository has three parts:
- Additional services added as patches into the Ambari installer. This is "the payload". The src and bin subdirectories.
- Deployment tools for amazon and generic systems to automate the deployment and speed up testing. The deployment subdirectory.
- Development tools and tests for developers of this project. The dev and tests subdirectories.

We also endeavor to provide an extensive [wiki documentation](https://github.com/KaveIO/AmbariKave/wiki)

Installation (on the 'ambari node' of your cluster, or one large machine)
=========================================================================

* AmbariKave is intended to be installed within a large cluster of machines. For installation on one machine, consider [KaveToolbox](http://github.com/KaveIO/KaveToolbox)

* To download and install a released version of AmbariKave from the repos server: http://repos.kave.io , e.g. 1.2-Beta, with username repos and password kaverepos
```
yum -y install wget curl tar zip unzip gzip
wget http://repos:kaverepos@repos.kave.io/centos6/AmbariKave/1.2-Beta/ambarikave-installer-centos6-1.2-Beta.sh
sudo bash ambarikave-installer-centos6-1.2-Beta.sh
```

( NB: the repository server uses a semi-private password only as a means of avoiding robots and reducing DOS attacks
  this password is intended to be widely known and is used here as an extension of the URL )

* OR to install the HEAD from git: example given with ssh copying from this github repo.
```
#test ssh keys with
ssh -T git@github.com
#if this works,
git clone git@github.com:KaveIO/AmbariKave.git
# Once you have a local checkout, install it with:
sudo service iptables stop
sudo chkconfig iptables off
cd AmbariKave
sudo dev/install.sh
sudo dev/patch.sh
sudo ambari-server start
```

Then to provision your cluster go to: http://YOUR_AMBARI_NODE:8080 or deploy using a blueprint, see https://cwiki.apache.org/confluence/display/AMBARI/Blueprints


Update our patches
====================

If you have the head checked out from git, you can update with:

Connect to your ambari/admin node
```
sudo where/I/checked/out/ambari/dev/pull-update.sh
```
pull-update also respects git branches, as a command-line argument and is linked into the way we do automated deployment and testing

To update between released versions, simply install the new version over the old version after stopping the ambari server:
```
sudo ambari-server stop
wget http://repos:kaverepos@repos.kave.io/centos6/AmbariKave/1.2-Beta/ambarikave-installer-centos6-1.2-Beta.sh
sudo bash ambarikave-installer-centos6-1.2-Beta.sh
```

( NB: the repository server uses a semi-private password only as a means of avoiding robots and reducing DOS attacks
  this password is intended to be widely known and is used here as an extension of the URL )

Installation of a full cluster
==============================

If you have taken the released version, go to http://YOUR_AMBARI_NODE:8080 or deploy using a blueprint, see https://cwiki.apache.org/confluence/display/AMBARI/Blueprints
If you have git access, and are working from the git version, See the wiki.

Deployment tools
==============================

See the deployment subdirectory, or the deployment tarball kept separately

Internet during installation, firewalls and nearside cache/mirror options
-------------------------------------------------------------------------

Ideally all of your nodes will have access to the internet during installation in order to download software.

If this is not the case, you can, possibly, implement a near-side cache/mirror of all required software. This is not very easy, but once it is done one time, you can keep it for later.
* Centos6: [Howto](https://ostechnix.wordpress.com/2013/01/05/setup-local-yum-server-in-centos-6-x-rhel-6-x-scientific-linux-6-x/)
* EPEL: [Mirror FAQ](http://www.cyberciti.biz/faq/fedora-sl-centos-redhat6-enable-epel-repo/) , [Mirroring](https://fedoraproject.org/wiki/Infrastructure/Mirroring)
* Ambari: [Local Repositories](https://ambari.apache.org/1.2.1/installing-hadoop-using-ambari/content/ambari-chap1-6.html)  [Deploying HDP behind a firewall](http://docs.hortonworks.com/HDPDocuments/HDP1/HDP-1.2.1/bk_reference/content/reference_chap4.html)

To setup a local near-side cache for the KAVE tool stack is quite easy.
First either copy the entire repository website to your own internal apache server, or copy the contents of the directories to your own shared directory visible from every node.

```
mkdir -p /my/shared/dir
cd  /my/shared/dir
wget -R http://repos.kave.io/
```

Then create a /etc/kave/mirror file on each node with the new top-level directory to try first before looking for our website:
```
echo "/my/shared/dir" >> /etc/kave/mirror
echo "http://my/local/apache/mirror" >> /etc/kave/mirror
```

So long as the directory structure of the nearside cache is identical to our website, you can drop, remove or replace, any local packages you will never install from this directory structure, and update it as our repo server updates.