var com = com || {};
com.apress = com.apress || {};
com.apress.collection = com.apress.collection || {};

com.apress.collection.jobResultList = Backbone.Collection.extend({
  model: com.apress.model.jobResult,
  comparator: function(jobresult) {
    return -Date.parse(jobresult.get("startdate"));
  }
});
