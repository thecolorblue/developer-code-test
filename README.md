## CMA Code Test

A quick catalog of CMA artwork. 

Folders:

`src` : Angular application code
`src/assets`: static assets for the angular app. This includes images (`src/assets/images`) and the artwork from the SQLite database (`src/assets/artwork.json`)
`dist`: compiled Angular application; this can be hosted on any static server to view the application

### Running Locally

The `/dist` folder is a compiled version of the app with everything it needs. You can use your favorite static server. Try `python -m SimpleHTTPServer 8000` in the `dist/code-test` folder.

#### For development

Runing `ng serve` will build the angular application, create a local server serving the app, and watch the files in `src` for changes. When a file in `src` is updated, the app will be recompiled and the browser will refresh the page. 