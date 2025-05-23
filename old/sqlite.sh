#!/bin/bash

confFile=./test.conf
DB=./identifier.sqlite
defPort=22
defRsa=~/.ssh/id_rsa
TABLE=param
man=./man.txt
lastID=$(sqlite3 $DB "SELECT rowid from $TABLE order by ROWID DESC limit 1")

RED='\033[0;31m'
GREEN='\033[0;32m'
NORMAL='\033[0m'

function addConf {
  read -e -p "Enter hostname: " Hostname
  Check=$(sqlite3 $DB "select hostname FROM $TABLE where Hostname='$Hostname'")
  if [ $Hostname == $Check ] 2> /dev/null
  then
    echo -e "${RED}Error: Hostname $Hostname alredy exist";
    exit 1
  fi
  function validAddress {
    for (( i=0; i<3; i++ ))
    do
      read -p "Enter IP address: " ip_addr
      read valid <<< $( awk -v ip="$ip_addr" '
      BEGIN { n=split(ip, i,"."); e = 0;
      if (6 < length(ip) && length(ip) < 16 && n == 4 && i[4] > 0 && i[1] > 0){
      for(z in i){if (i[z] !~ /[0-9]{1,3}/ || i[z] > 255){e=1;break;}}
      } else { e=1; } print(e);}')
      if [ $valid == 0 ]; then
        Address=$ip_addr
        break
      else
        echo -e "${RED}Fail: IP Invalid"
        echo -e "${NORMAL}"
      fi
    done
  }
  echo "IP address or Domain?
[1] IP Address
[2] Domain
Default IP address"
  read -p "Choose an option: " x
  case $x in
  [1]* ) validAddress;;
  [2]* ) read -p "Enter domain: " Address ;;
  *) validAddress;;
  esac
  read -e -p "Enter Username: " Username
  while true; do
  		read -p "Using default identity file? [Y/n] " yn
  		case $yn in
  			[Yy]* ) Rsa=$defRsa; break;;
  			[Nn]* ) read -e -p "Enter path to rsa file (enter only absolute path): " Rsa
  				break;;
  			* ) Rsa=$defRsa; break ;;
  		esac
  	done
  while true; do
  	read -p "Using default port? [Y/n] " yn
  	case $yn in
  		[Yy]* ) Port=$defPort ;break;;
  		[Nn]* )	read -e -p "Enter port: " Port; break;;
  		* ) Port=$defPort; break;;
  	esac
  done
  echo -e "${GREEN}"
  echo "Hostname: $Hostname"
  echo "IP Address: $Address"
  echo "Username: $Username"
  echo "Port: $Port"
  echo "ID rsa file: $Rsa"
  echo -e "${NORMAL}"
  while true
  do
  	read -p "It the config correct? [y/N] " yn
  	case $yn in
  		[Yy]* ) sqlite3 $DB "insert into $TABLE values($(( $lastID+1 )), '$Hostname', '$Address', '$Username', '$Rsa', $Port);"; writeConf; exit 0;;
  		[Nn]* ) exit 1;;
  		* ) exit 1;;
  	esac
  done
}
function writeConf {
  cat /dev/null > $confFile
  for i in $(sqlite3 $DB "select * from $TABLE;")
  do
    echo "" >> $confFile
    echo "Host $(echo $i |awk -F'|' '{print $2}')" >> $confFile
    echo "  HostName $(echo $i |awk -F'|' '{print $3}')" >> $confFile
    echo "  User $(echo $i |awk -F'|' '{print $4}')" >> $confFile
    echo "  Port $(echo $i |awk -F'|' '{print $6}')" >> $confFile
    echo "  IdentityFile $(echo $i |awk -F'|' '{print $5}')" >> $confFile
  done
}
#function insertConf {
#  sqlite3 $DB "insert into $TABLE values($(( $lastID+1 )), '$Hostname', '$Address', '$Username', '$Rsa', $Port);"
#}
function delConf {
    if [ -z $1 ]
  	then
  		read -e -p "Enter hostname: " Hostname
  		Check=$(sqlite3 $DB "select hostname FROM $TABLE where Hostname='$Hostname'")
  		if [ $Hostname == $Check ] 2> /dev/null
  		then
  		  echo -e "${GREEN}Hostname: $Hostname
 IP Address: $(sqlite3 $DB "select addres from $TABLE where hostname='$Hostname'")
 Username: $(sqlite3 $DB "select username from $TABLE where hostname='$Hostname'")"
        echo -e "${RED}"
  		  read -p "Delete this config? [y/N] " yn
  		  while true; do
  		    case $yn in
  		      [Yy]* ) sqlite3 $DB "delete from param where hostname='$Hostname'";;
  		      [Nn]* ) exit 0;;
  		      * ) exit 0;;
  		    esac
  		  done
  		else
  		  echo -e "${RED}Hostname not found!"
  		fi
  	else
  		Check=$(sqlite3 $DB "select hostname FROM $TABLE where Hostname='$1'")
  		if [ $1 == $Check ] 2> /dev/null
  		then
  		  echo -e "${GREEN}Hostname: $Hostname
 IP Address: $(sqlite3 $DB "select addres from $TABLE where hostname='$1'")
 Username: $(sqlite3 $DB "select username from $TABLE where hostname='$1'")"
        echo -e "${RED}"
  		  read -p "Delete this config? [y/N] " yn
  		  while true; do
  		    case $yn in
  		      [Yy]* ) sqlite3 $DB "delete from param where hostname='$1'";;
  		      [Nn]* ) exit 0;;
  		      * ) exit 0;;
  		    esac
  		  done
  		else
  		  echo -e "${RED}Hostname not found!"
  		fi
  	fi
}
function searchConf {
  if [ -z $1 ]
	  then
		echo -e "${RED}Hostname not specified!"
		exit 1
	else
	  for i in $(sqlite3 $DB "select id, hostname, addres from $TABLE" |grep $1 |awk -F'|' '{print $1}')
	  do
      echo -e "${GREEN}| Hostname: $(sqlite3 $DB "select hostname from $TABLE where id=$i") ;; IP address: $(sqlite3 $DB "select addres from $TABLE where id=$i") ;; Port: $(sqlite3 $DB "select port from $TABLE where id=$i") |"
    done
	fi
}
function confirmConf {
    echo -e "${GREEN} Hostname: $Hostname"
    echo -e "${GREEN} IP Address: $Address"
    echo -e "${GREEN} Username: $Username"
    echo -e "${GREEN} Port: $Port"
    echo -e "${GREEN} ID rsa file: $Rsa"
}
if [ -n "$1" ]
then
	while [ -n "$1" ]; do
		case "$1" in
			--help|-h) cat $man; exit 0;;
			--search|-s) searchConf $2 2> /dev/null; exit 0;;
			--add|-a) addConf; exit 0;;
#     --additional-parameters) addConf;;
#			--create-keys|-c) create-keys;;

			--delete|-d) delConf $2; writeConf; exit 0;;
	    --write|-w) writeConf; exit 0;;
			*) echo "illegal option $1"; cat $man; exit 2;;
		esac
		shift
	done
else
	addConf
fi
exit 0
