var com = com || {};
com.apress = com.apress || {};
com.apress.model = com.apress.model || {};

com.apress.model.jobResult = Backbone.Model.extend({
  defaults: {
    jobid: '',
    jobunit: '',
    jobname: '',
    startdate: '',
    stopdate: ''
  }
});
