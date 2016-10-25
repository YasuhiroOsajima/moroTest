var express = require('express');
var fs = require('fs');
var path = require('path');
var mongoose = require('mongoose');
var mongo = require('./mongo');
var ConfigFile = require('config');
var request = require('request');


//Jenkins REST API
var ENDPOINT_BASE = 'http://127.0.0.1:8080/job/';
var headers = {'Content-Type':'application/json'}


exports.getjob = function(req, res){
  var jobname = req.query.jobname;

  var get_options = {
    url: ENDPOINT_BASE + jobname + '/api/json/builds?depth=1',
    method: 'GET',
    headers: headers,
    auth: {
      user: ConfigFile.config.jenkins_user,
      password: ConfigFile.config.jenkins_password
    },
    json: true,
  }

  request(get_options, function (error, response, body) {
    var respjobid = response["body"]["builds"][0]["number"];
    var respresult = response["body"]["builds"][0]["result"];

    var data = {"respjobid": respjobid, "respresult": respresult}
    console.log(data);

    res.status(200);
    res.json(data);
  })
};


exports.runjob = function(req, res){
  var jobname = req.body.jobname;

  var post_options = {
    url: ENDPOINT_BASE + jobname + '/build',
    method: 'POST',
    headers: headers,
    auth: {
      user: ConfigFile.config.jenkins_user,
      password: ConfigFile.config.jenkins_password
    },
    json: true,
  }

  request(post_options, function (error, response, body) {
    console.log(response["headers"]["location"]);
    var locationsplit = response["headers"]["location"].split('/');
    var jobid = locationsplit[locationsplit.length - 2];

    var data = {"jobid": jobid};
    console.log(data);

    res.status(200);
    res.json(data);
  })
};


//MongoDB
//POST
exports.saveresult = function (req, res){
  var jobid = req.body.jobid;
  var job_name = req.body.jobname;
  var jobrun_id = new mongoose.Types.ObjectId();

  mongo.registerjobResult(req, jobrun_id);

  var logfile = ConfigFile.config.jenkins_dir + "/jobs/" + job_name + '/builds/' + jobid + "/log";
  //var logfilepath = path.resolve(logfile);
  var read = fs.createReadStream(logfile);
  read.on('data', function (data) {
    var resultdata = data.toString();
    console.log(jobrun_id);
    console.log(typeof resultdata);
    mongo.createjobResultData(jobrun_id, resultdata);
  });

  res.send(200);
};

//GET
exports.jobresult_get_byunit = function(req, res) {
  mongo.getjobResult_byjobunit(req, res);
};

exports.jobresult_get_byname = function(req, res) {
  mongo.getjobResult_byjobname(req, res);
};

exports.jobresultdata_get = function(req, res) {
  mongo.getjobResultData(req, res);
};


exports.jobresultdata_search = function(req, res) {
  mongo.getjobResultData_byData(req, res);
};

//DELETE
exports.deleteresult = function (req, res){
  var jobrunid = req.query.jobrunid;
  var jobrun_id = new mongoose.Types.ObjectId(jobrunid);

  mongo.deletejobResult(jobrun_id);
  mongo.deletejobResultData(jobrun_id);
  res.send(200);
};


//send file
exports.index = function(req, res){
  console.log(__dirname + '/../html/tool.html');
  var indexfilepath = path.resolve(__dirname + '/../html/tool.html');
  res.sendFile(indexfilepath);
};

exports.imageget = function(req, res){
  var imagename = req.path;
  var targetimage = __dirname + '/..' + imagename;
  console.log(targetimage);
  var imagefilepath = path.resolve(targetimage);
  res.sendfile(imagefilepath);
};

exports.favicon = function(req, res){
  console.log(__dirname + '/../images/favicon.ico');
  var favifilepath = path.resolve(__dirname + '/../images/favicon.ico');
  res.sendfile(favifilepath);
};

