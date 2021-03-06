App architecture
================

Class diagram
-------------
.. image:: flowcharts/uml.svg

Peer
----
Peer is the main communication endpoint for the application. It is created from the **Client** and **Server** classes. It creates objects from those two classes. It is also responsible for handling the heartbeat messages that are used for checking availability. If the other peer that the file is being sent to is offline, **a background process is created** which will attempt to send the file on a specified interval until a certain amount of time **specified by the user** passes. The file that is to be sent is **encrypted** until the receiving peer is ready. If the main windows is closed so is this process.

Client
------
Client handles **file sending** and heartbeat communication. Besides that he also handles the creation of ssl sockets that are used for communicating securely. The **TLS protocol** is used for creating a secure channel between the peers. The client **requires the servers certificate** in order to communicate with him. The client is also responsible for building the header for the file transfer (:doc:`header`).

Server
------
Server handles heartbeat communication and **file receiving**. Same as the client it also handles the creation of ssl sockets. Sockets are configured such that only cipher suites with **AES symmetric encryption** and **GCM block mode** are chosen. The server also **requires the clients certificate** in order to start communicating. The server part of the peer always runs in a **separate thread**, that way the main program is not being blocked by the server listening to incoming connections.

Heartbeat communication
-----------------------
It is used to check whether the other peer is available by sending the `HEARTBEAT` flag defined in the `Flags` class (:doc:`source.peer`). If the other peer send the flag back the file sending process can begin.

Database
--------
The database holds the paths to certificates and the private key of the user. The private key is encrypted using a password. It also holds the cached address of the peers that are manually entered. The database is also encrypted using a password with a python wrapper using the `sqlcipher <https://github.com/sqlcipher/sqlcipher>`_ binary. It is encrypted using **AES 256** with a key generated from a password which is entered by the user at the start of the application.

MainGui
-------
It is the frontend of the application. It is built using `tkinter <https://docs.python.org/3/library/tkinter.html>`_ library. File/directory paths and socket address **are validated** before the inputs are being saved. If the peer is going receive a file he **must click a button** before he will receive it. If the peer is sending a file a new window is created displaying information about the file sending process and peer availability.



