29/03/2024 - LGMVentura

This tutorial tells you how to do THE thing!

## Installing requirements
Install nvm for node.js: https://github.com/nvm-sh/nvm

If an older version of npm is already installed, remove it:
```
sudo apt purge nodejs npm
```

On Ubuntu 22.04, the following worked:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm


nvm install node
```

## Creating the project
https://openlayers.org/doc/quickstart.html

```
npm create ol-app my-app
cd my-app
npm start
```

This will run the server from which the OpenLayers (map stuff) will run with html and javascript. If we open the html file directly into the browser, it will block the js content for security reasons. Using the browser when using `npm start`, in the last case, `http://localhost:5173/`, it will run the file as if it were on the web, running the script too.

The layout can be edited in the html and the animation functions in the js file. Follow the examples here.

## Rendering video frames
Another js script will generate the frames, but it will be run from `node` in the background. See the example `map_animations/move_view/captureMapFrames.js`. This will call the server `http://localhost:5173/` (change if needed) and capture the frames from main.js. captureMapFrames.js does not know about main.js. So you have to start main.js by starting the project `npm start` from the project folder.

To save the frames as images, pupperteer is needed. This can be installed (from the project folder) using `npm install puppeteer`. Otherwise, captureMapFrames.js will throuw an error.

Basically, everything that is needed for the project has to be installed inside the project.


