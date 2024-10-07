.PHONY: all sender receiver ncat lossy_link data_sender clean

all: sender receiver ncat lossy_link data_sender

sender:
	gnome-terminal -- python3 Sender.py

receiver:
	gnome-terminal -- python3 Receiver.py

ncat:
	gnome-terminal -- ncat --recv-only -u -l 54321

lossy_link:
	gnome-terminal -- ./lossy_link-linux 127.0.0.1:9092 127.0.0.1:7022

data_sender:
	echo "Plaese RUN this command seperatly `seq 1000 | while read; do sleep 0.01; echo \"\$$REPLY\"; done | ncat --send-only -u 127.0.0.1 12345`"

clean:
	rm -f sender_script.sh
