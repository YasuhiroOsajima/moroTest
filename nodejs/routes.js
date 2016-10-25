var path = require('path');
var webapi = require('./webapi');


exports.images = function(req, res) {
  var accesspath = req.path;
  console.log(accesspath);
  webapi.imageget(req, res);
  }

};

