#!/bin/bash
# script to update RPMs, restart apache and change log ownership
# to be run as atlpan on aipanda043
# Contact Jaroslava.Schovancova@cern.ch with questions. 

echo "### Running $(basename $0) as $(whoami) @ $(hostname) at $(date)"
PACKAGE1="twdev-bigpandamon-lsst"
PACKAGE2="twdev-bigpandamon-core"


### Define functions ###
function check_package_installation {
    package=$1
    rpm -qa | grep $package
}

function install_package {
    package=$1
    sudo yum clean all
    sudo yum --assumeyes install $package
}

function update_package {
    package=$1
    sudo yum clean all
    sudo yum --assumeyes update $package
}

function publish_package_version {
    package=$1
    version_file=/data/version/$package
    check_package_installation $package > $version_file
}
### End of: Define functions ###


### Update bigpandamon RPMs
echo "### Will update RPMs"
echo " ... package $PACKAGE1 ..."
if [ -z $(check_package_installation $PACKAGE1) ]; then
    install_package $PACKAGE1
else
    update_package $PACKAGE1
fi
publish_package_version $PACKAGE1

echo " ... package $PACKAGE2 ..."
if [ -z $(check_package_installation $PACKAGE2) ]; then
    install_package $PACKAGE2
else
    update_package $PACKAGE2
fi
publish_package_version $PACKAGE2
echo "### ... after RPMs update "

### Restart apache
echo "### Will restart apache"
sudo service httpd restart
echo "### ... after apache restart"


### Change log files ownership
echo "### Will change bigpandamon log files ownership"
sudo chown apache:apache -R /data/bigpandamon_virtualhosts/atlas/logs/* 
sudo chown apache:apache -R /data/bigpandamon_virtualhosts/devprodsys2/logs/*
sudo chown apache:apache -R /data/wenaus/bigpandamon_virtualhosts/twrpm/logs/*
## sudo chown apache:apache -R /data/atlpan/bigpandamon/var/log/* 
## sudo chown apache:apache -R /data/bigpandamon_virtualhosts/jedimon/logs/* 
echo "### ... after bigpandamon log files ownership change"

echo ''

echo "### Finished running $(basename $0) as $(whoami) @ $(hostname) at $(date)"


