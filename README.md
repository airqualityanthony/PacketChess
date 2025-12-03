## PacketChess
### Packet Chess for BPQ
---
[MIT License](https://opensource.org/license/mit/)

Packet Chess for Packet Radio.  It's made to work with the [BPQ32 Packet Switch from G8BPQ](https://www.cantab.net/users/john.wiseman/Documents/BPQ32.html).  It requires that you have a basic Python3 install which most everyone should who runs modern Linux.

Packet Chess when running on your packet system will look like this:
```
*** Connected to Chess        
-=- Games -=-


```

## Installation
Download and install PacketChess to your system:
```
git clone https://github.com/airqualityanthony/PacketChess.git
```

Configure BPQ to connect to external application ports[^1]:
```
; Telnet Port
PORT
PORTNUM=15
 ID=Telnet
 DRIVER=TELNET
 ; ... etc ...
 CONFIG
  ; external application ports, zero indexed!
  CMDPORT=6000 6001 6002 6003 6004 6005 6006 6007 6008 6009 6010
ENDPORT

; Application Lines
APPLICATION 1,BBS,,N0CALL-1,CALBBS,255
APPLICATION 3,CHAT,,N0CALL-11,CALCHT,255

; External Applications
APPLICATION 5,CHESS,C 15 HOST 1 S,N0CAL-5,CALCHESS,255
```
Note: CMDPORT= ports are zero indexed, such that "C 15 HOST 1 S" will connect to port 15 (Telnet) in the example config, and then connect to local host on command port 1 which is the second port 6001 in the CMDPORT= list.
**The "S" in the connect string tells BPQ to return the user to the node when they exit packetchess.**

## inetd server
You can run PacketChess from inet.d or xinet.d as a TCP service[^2]:
```
service packetchess
{
	disable		= no
	protocol	= tcp
	port		= 6001
	server		= /home/bpquser/packetchess.py
	user		= bpquser
	socket_type	= stream
	wait		= no
}
```
And adding packetchess to /etc/services.


## systemd server
You can run packetchess from systemd as a socket service[^3]:

Edit the supplied *packetchess.socket* and *packetchess@.service* to match the _path, username and port_ of your configuration.
Copy *packetchess.socket* and *packetchess@.service* to */etc/systemd/system/*.

Then enable the service:
```
sudo systemctl daemon-reload
sudo systemctl enable packetchess.socket
sudo systemctl start packetchess.socket
```

[^1]: [LinBPQ Applications Interface](https://www.cantab.net/users/john.wiseman/Documents/LinBPQ%20Applications%20Interface.html)
[^2]: [xinet.d](https://en.wikipedia.org/wiki/Xinetd)
[^3]: [systemd](https://en.wikipedia.org/wiki/Systemd)
