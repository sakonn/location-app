#!/usr/bin/env bash

hostsFile="/etc/hosts"

yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

remove() {
    if [ -n "$(grep -P "[[:space:]]$hostname" /etc/hosts)" ];
    then
        try sudo sed -ie "/[[:space:]]$hostname/d" "$hostsFile";
        echo "REMOVE: $hostname removed from $hostsFile.";
    else
        yell "REMOVE: $hostname was not found in $hostsFile";
    fi
}

add() {
    if [ -n "$(grep -P "[[:space:]]$hostname" /etc/hosts)" ];
    then
        yell "ADD: $hostname, already exists: $(grep $hostname $hostsFile)";
    else
        try printf "%s\t%s\n" "$ip" "$hostname" | sudo tee -a "$hostsFile" > /dev/null;

        if [ -n "$(grep "$hostname" /etc/hosts)" ];
        then
            echo "ADD: $hostname was added succesfully.";
        else
            die "ADD: Failed to add $hostname";
        fi
    fi
}

echo "### hosts update: start"
now="$(date +"%Y-%m-%d-%I-%M-%S")"
cp /etc/hosts /tmp/hosts."$now".backup
while IFS='	' read -r ip hostname || [[ -n "$line" ]]; do
    if [[ ! -z $hostname ]];
    then
        remove $hostname;
        add $hostname;
    fi
done < "${BASH_SOURCE%/*}"/domains.txt

echo "### hosts update: finished";
echo "### less /etc/hosts";
less -X -F /etc/hosts;
