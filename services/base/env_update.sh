#!/bin/sh

if [ $# -ne 2 ]
then
	echo "Usage: env_update [file_to_interpolate] [output_file]";
	exit 1;
fi

echo "Interpolating env variables in $1";

env | sed 's/[\%]/\\&/g;s/\([^=]*\)=\(.*\)/s%${\1}%\2%/' > sed.script;

cat $1 | sed -f sed.script > $2;

rm sed.script;
