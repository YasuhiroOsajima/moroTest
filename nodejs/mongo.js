var mongoose = require('mongoose');
var ConfigFile = require('config');

mongouri="mongodb://" + ConfigFile.config.mongo_user + ":" + ConfigFile.config.mongo_password + "@" + ConfigFile.config.mongo_host + "/moroTest";
mongoose.connect(mongouri);


//jobresult
var jobresultSchema = new mongoose.Schema({
  jobunit: {type:String, required: true},
  jobname: {type:String, required: true},
  startdate: {type:Date, required: true},
  stopdate: {type:Date, required: true},
});
var jobResult = mongoose.model('jobresult', jobresultSchema);

exports.getjobResult_byjobunit = function(req, res) {
  var job_unit = req.query.jobunit;

  jobResult.find({jobunit: new RegExp(".*"+job_unit+".*")}, function(err, items) {
    if (err) {console.log(err);}
    res.header({"Content-Type": "application/json",
                "charset": "utf-8"});
    res.json(items);
  });
};

exports.getjobResult_byjobname = function(req, res) {
  var job_name = req.query.jobname;

  jobResult.find({jobname: new RegExp(".*"+job_name+".*")}, function(err, items) {
    if (err) {console.log(err);}
    res.header({"Content-Type": "application/json",
                "charset": "utf-8"});
    res.json(items);
  });
};

//exports.findjobResult = function(req, res) {
//  var jobrunid = req.query.jobrunid;
//  var jobrun_id = new mongoose.Types.ObjectId(jobrunid);
//
//  jobResult.find({_id: jobrun_id}, function(err, items) {
//    if (err) {console.log(err);}
//    res.header({"Content-Type": "application/json",
//                "charset": "utf-8"});
//    res.json(items);
//  });
//};

exports.registerjobResult = function(req, jobrun_id) {
  var job_unit = req.body.jobunit;
  var job_name = req.body.jobname;
  var start_date = req.body.startdate;
  var stop_date = req.body.stopdate;

  var new_jobresult = new jobResult({
    _id: jobrun_id,
    jobunit: job_unit,
    jobname: job_name,
    startdate: start_date,
    stopdate: stop_date,
  });

  new_jobresult.save(function(err) {
    if (err) {console.log(err);}
  });
};

exports.deletejobResult = function(jobrun_id) {
  jobResult.remove({_id: jobrun_id}, function(err) {
    if(err) {console.log(err);}
  });
};


//jobresult_data
var jobResultDataSchema = new mongoose.Schema({
  resultlog: {type:String}
});
var jobResultData = mongoose.model('jobresultdata', jobResultDataSchema);

exports.getjobResultData = function(req, res) {
  var jobrunid = req.query.jobrunid;
  console.log(jobrunid);
  var jobrun_id = new mongoose.Types.ObjectId(jobrunid);

  jobResultData.find({_id: jobrun_id}, function(err, items) {
    if (err) { console.log(err); }
    res.header({"Content-Type": "application/json",
                "charset": "utf-8"});
    console.log(items);
    res.json(items);
  });
};

exports.getjobResultData_byData = function(req, res) {
  var log_data = req.query.logdata;
  var jobrun_ids = [];

  jobResultData.find({data: new RegExp(".*"+log_data+".*")}, function(err, items) {
    if (err) { console.log(err); }
    for (i=0; i<items.length; i++) {
      jobrun_ids.push(items[i].id);
    }
    res.json(jobrun_ids);
  });
};

exports.createjobResultData = function(jobrun_id, resultdata) {
  var new_jobresultdata = new jobResultData({
    _id: jobrun_id,
    resultlog: resultdata
  });

  new_jobresultdata.save(function(err) {
    if (err) { console.log(err); }
  });
};

//exports.updatejobResultData = function(req, res) {
//  var jobrunid = req.query.jobrunid;
//  var jobrun_id = new mongoose.Types.ObjectId(jobrunid);
//  var resultdata = req.body.resultdata;
//
//  jobResultData.update(
//    {_id: jobrun_id},
//    { $set: {data: resultdata}},
//    { upsert: false, multi: false }, function(err) {
//      if(err) {console.log(err);}
//    }
//  );
//};

exports.deletejobResultData = function(jobrun_id) {
  var jobrun_id = new mongoose.Types.ObjectId(jobrunid);

  jobResultData.remove({_id: jobrun_id}, function(err) {
    if(err) {console.log(err);}
  });
};


