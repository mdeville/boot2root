#!/bin/bash

if [[ $1 == "" ]]
then
	1>&2 echo "usage: $0 \$TARGET"
	exit 1
fi

function concat () {
	for word in $(cat $1)
	do
		printf $word
	done
}

for file in soluce*
do
	password=$(concat $file)
	echo "Attempting to login into thor@$1 with password $password"
	sshpass -p "$password" ssh thor@$1
done
