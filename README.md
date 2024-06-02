# Reel
### In the sea of browsers you can always hook someone...

# Description
FishermanC2 is a browser hooking variant of normal c2 frameworks.   
It allows you to gather info from hooked browsers and gain complete js rce on the browser, allowing phishing, clickjacking and many more serious attacks.

## Setup
- Download nginx.
- Run the setup script to configure admin username and password, and get key and certificate requried for the nginx routing.
```bash
$ ./setup.sh
```
- Make sure everything is set for nginx by running
```bash
$ nginx -t
```
- And then run it with
```bash
$ nginx
```
- Run the flask application by using the `local.json` configurations or simply running
```bash
$ python api/server.py
```
- OPTIONAL: Run the demo server for an easy experimentation with the app using
```bash
$ python demo/app.py
```

