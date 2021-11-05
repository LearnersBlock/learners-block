#!/bin/bash

# Built mirroring Balena image setup:
# https://github.com/balena-io-library/base-images/blob/ \
# 	72e384b6f3cdd5e966bb39811ed61cb4aba9d587/balena-base-images/ \
#	armv7hf/alpine/3.14/run/entry.sh

# This command only works in privileged container
tmp_mount='/tmp/_balena'
mkdir -p "$tmp_mount"
if mount -t devtmpfs none "$tmp_mount" &> /dev/null; then
	PRIVILEGED=true
	umount "$tmp_mount"
else
	PRIVILEGED=false
fi
rm -rf "$tmp_mount"

function mount_dev()
{
	tmp_dir='/tmp/tmpmount'
	mkdir -p "$tmp_dir"
	mount -t devtmpfs none "$tmp_dir"
	mkdir -p "$tmp_dir/shm"
	mount --move /dev/shm "$tmp_dir/shm"
	mkdir -p "$tmp_dir/mqueue"
	mount --move /dev/mqueue "$tmp_dir/mqueue"
	mkdir -p "$tmp_dir/pts"
	mount --move /dev/pts "$tmp_dir/pts"
	touch "$tmp_dir/console"
	mount --move /dev/console "$tmp_dir/console"
	umount /dev || true
	mount --move "$tmp_dir" /dev

	# Since the devpts is mounted with -o newinstance by Docker, we need to make
	# /dev/ptmx point to its ptmx.
	# ref: https://www.kernel.org/doc/Documentation/filesystems/devpts.txt
	ln -sf /dev/pts/ptmx /dev/ptmx
	mount -t debugfs nodev /sys/kernel/debug
}

function start_udev()
{
	if [ "$UDEV" == "on" ]; then
		if $PRIVILEGED; then
			mount_dev
			unshare --net udevd --daemon &> /dev/null
			udevadm trigger &> /dev/null
		else
			echo "Unable to start udev, container must be run in privileged mode to start udev!"
		fi
	fi
}

function init()
{
	# echo error message, when executable file doesn't exist.
	if [ -n "$1" ]; then
		if CMD=$(command -v "$1" 2>/dev/null); then
			shift
			exec "$CMD" "$@"
		else
			echo "Command not found: $1"
			exit 1
		fi
	fi
}

UDEV=$(echo "$UDEV" | awk '{print tolower($0)}')

case "$UDEV" in
	'1' | 'true')
		UDEV='on'
	;;
esac

start_udev
init "$@"
