#!/bin/sh

if [ $# -ne 2 ]
then
	echo "Usage: env_update [file_to_interpolate] [output_file]";
	exit 1;
fi

SED_SCRIPT="${HOME}/sed.script"

echo "Interpolating env variables in $1";

env | sed 's/[\%]/\\&/g;s/\([^=]*\)=\(.*\)/s%${\1}%\2%/' > "${SED_SCRIPT}";

cat $1 | sed -f "${SED_SCRIPT}" > $2;

rm "${SED_SCRIPT}";
