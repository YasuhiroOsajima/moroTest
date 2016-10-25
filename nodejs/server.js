  // require packages
var express = require('express');
var logger = require('morgan');
var path = require('path');
var ConfigFile = require('config');

  // for REST API
var bodyParser = require('body-parser');
var methodOverride = require('method-override');
var errorHandler = require('express-error-handler');
var mongoose = require('mongoose');

  //original method
var webapi = require('./webapi');

  //create app server
var app = express();
app.use(logger());
app.use(express.static(path.resolve(__dirname + '/../')));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(methodOverride());
app.use(errorHandler());

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS");
  next();
});

app.get('/', webapi.index);

app.post('/runjob', webapi.runjob);
app.get('/getjob', webapi.getjob);

app.post('/saveresult', webapi.saveresult);
app.get('/jobresult_get_byunit', webapi.jobresult_get_byunit);
app.get('/jobresult_get_byname', webapi.jobresult_get_byname);
app.get('/jobresultdata_get', webapi.jobresultdata_get);
app.get('/jobresultdata_search', webapi.jobresultdata_search);
app.delete('/deleteresult', webapi.deleteresult);

app.get('/favicon.ico', webapi.favicon);
app.get('/images/*', webapi.imageget);

app.listen(ConfigFile.config.listen_port);


