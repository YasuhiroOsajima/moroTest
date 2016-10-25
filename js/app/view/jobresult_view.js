var com = com || {};
com.apress = com.apress || {};
com.apress.view = com.apress.view || {};


com.apress.view.jobResultView = Backbone.View.extend({
  tagName: 'li',
  className: 'jobresult',
  template: _.template( $('#jobresult_entry').html() ),
  events: {
    'click': 'click'
  },
  click: function(e) {
    console.log(this.el.id);
    printLogview(this.el.id);
  },

  render: function() {
    this.el.id = this.model.toJSON()._id;
    var template = this.template( this.model.toJSON() );
    this.$el.html(template);

    this.$el.css({
     'background': '#dcdcdc',
     'border-top': '#fff 1px solid',
     'border-left': '#fff 1px solid',
     'border-right': '#999 1px solid',
     'border-bottom': '#999 1px solid'
    });

    return this;
  }
});


com.apress.view.jobResultsView = Backbone.View.extend({
  tagName: 'ul',
  id: 'jobresultlist',

  render: function() {
    console.log(this);
    this.collection.each(function(jobresult) {
      var resultView = new com.apress.view.jobResultView({ model: jobresult });
      this.$el.append(resultView.render().el);
    }, this);

    this.$el.css({
     //'background': '#ebafff',
     //'border-top': '#fff 1px solid',
     //'border-left': '#fff 1px solid',
     //'border-right': '#999 1px solid',
     //'border-bottom': '#999 1px solid',
     'margin': '0 0'
    });

    return this;
  }
});


function printLogview(jobid) {
  $.ajax({
    type: "GET",
    url: "/jobresultdata_get",
    data: {"jobrunid": jobid},
    async: false,
    cache: false,
    success : function(json, status) {
      if (json[0]) {
        var joblog = json["0"]["resultlog"];
        $('#logview').html(joblog);
      } else {
        $('#logview').empty();
      }
    }
  });
};


