var headerurl = document.origin.slice(6);

//var jobstatus;
function getjobstatus(jobname){
  return $.ajax({
           type: "GET",
           url: "/getjob",
           data: {"jobname": jobname},
           async: false,
           cache: false,
         });
}


function runjob(jobname){
  return $.ajax({
           type: "POST",
           url: "/runjob",
           data: {"jobname": jobname},
           async: true,
           cache: false,
         });
}


function createDateobj() {
  var now = new Date();
  var yyyymmddhhmmss = now.getFullYear()+'/'+
                       ('0'+(now.getMonth()+1) ).slice(-2)+'/'+
                       ('0'+now.getDate()).slice(-2)+' '+
                       ('0'+now.getHours()).slice(-2)+':'+
                       ('0'+now.getMinutes()).slice(-2)+':'+
                       ('0'+now.getSeconds()).slice(-2);
  return yyyymmddhhmmss;
}


function savejobresult(jobunit, jobname, startdate, stopdate, jobid) {
  return $.ajax({
           type: "POST",
           url: "/saveresult",
           data: {"jobunit": jobunit, "jobname": jobname, "startdate": startdate, "stopdate": stopdate, "jobid": jobid},
           async: false,
           cache: false,
         });
}


function Sleep( T ){ 
   var d1 = new Date().getTime(); 
   var d2 = new Date().getTime(); 
   while( d2 < d1+1000*T ){    //T秒待つ 
       d2=new Date().getTime(); 
   } 
   return; 
}


function wait_jobsuccess(jobname, jobid){
  var respjobid = 0;
  var respresult = null;
  do {
    getjobstatus(jobname).done(function(result) {
      respjobid = result["respjobid"];
      respresult = result["respresult"];
      console.log(respjobid);
      console.log(jobid);
      console.log(respresult);
    });
    Sleep(5);
  } while (respjobid!=jobid || respresult!="SUCCESS");
}


(function(){
  $('div#main').append('<img src="http://'+ headerurl +'/images/jenkins-wallpaper.jpg" width="400x">');
})();


function unit_name_empty(jobunit, jobname) {
  if (jobunit=='' && jobname=='') {
    $('div#main').empty();
    $('div#main').append('<img src="http://'+ headerurl +'/images/jenkins_oops.jpg" width="550x">');
    $('div#main').append('<input type="submit" value="すまん" id="suman">');

    $(function($) {
      $('input#suman').click(function() {
        $('div#main').empty();
        $('div#main').append('<img src="http://'+ headerurl +'/images/jenkins_eenyade.jpg" width="500x">');
      });
    });

    return false;
  } else {
    return true;
  }
}

// run job
$('input#run').click(function() {
  $('div#main').empty();
  $('div#logview').empty();

  $('div#main').append('<input type="text" name="jobunit" id="jobunit" placeholder="ジョブユニット"><br>');
  $('div#main').append('<input type="text" name="jobname" id="jobname" placeholder="ジョブ"><br>');
  $('div#main').append('<input type="submit" value="ゆけ" id="runsubmit">');
  $('div#main').append('<img src="http://'+ headerurl +'/images/jenkins_yaru.jpg" width="550x">');

  $(function($) {
    $('input#runsubmit').click(function() {
      var jobunit = $('input#jobunit').val();
      var jobname = $('input#jobname').val();
      if ( !unit_name_empty(jobunit, jobname) ) {return;}

      runjob(jobname).done(function(result) {
        var startdate = createDateobj();
        var jobid = result["jobid"];

        wait_jobsuccess(jobname, jobid);
        var stopdate = createDateobj();
        console.log("DEBUG");

        savejobresult(jobunit, jobname, startdate, stopdate, jobid);
        $('div#main img').remove();
        $('div#main').append('<img src="http://'+ headerurl +'/images/jenkins_tehepero.jpg" width="250x">');
      });
    });
  });

});



// get job
function printjobResults(allResultList) {
  var jobresultList = new com.apress.collection.jobResultList();

  for (i=0; i<allResultList.length; i++) {
    jobresultList.add(allResultList[i]);
  }

  console.log(jobresultList);
  var resultsView = new com.apress.view.jobResultsView({collection: jobresultList});
  $('#jobresult_main').html(resultsView.render().el);
};


function getjobresult_byunit(jobunit){
  return $.ajax({
           type: "GET",
           url: "/jobresult_get_byunit",
           data: {"jobunit": jobunit},
           async: false,
           cache: false,
         });
}


function getjobresult_byname(jobname){
  return $.ajax({
           type: "GET",
           url: "/jobresult_get_byname",
           data: {"jobname": jobname},
           async: false,
           cache: false,
         });
}


$('input#find').click(function() {
  $('div#main').empty();
  $('div#logview').empty();

  $('div#main').append('<input type="text" name="jobunit" id="jobunit" placeholder="ジョブユニット"><br>');
  $('div#main').append('<input type="text" name="jobname" id="jobname" placeholder="ジョブ"><br>');

  $('div#main').append('<input type="submit" value="こい" id="findsubmit">');
  $('div#main img').css('float', 'left');
  $('div#main img').css('overflow', 'auto');

  $('div#main').append('<div id="imagewrap"></div>');
  $('div#imagewrap').css('width', '100%');
  $('div#imagewrap').css('float', 'left');
  $('div#imagewrap').css('overflow', 'auto');

  $('div#imagewrap').append('<img src="http://' + headerurl + '/images/jenkins_miru.jpg" width="350x">');

  $('div#main').append('<section id="jobresult_main"></section>');
  $('section#jobresult_main').css('float', 'left');
  $('section#jobresult_main').css('overflow', 'auto');
  $('section#jobresult_main').css('width', '50%');
  $('section#jobresult_main').css('margin', '0 0');


  $(function($) {
    $('input#findsubmit').click(function() {
      var jobunit = $('input#jobunit').val();
      var jobname = $('input#jobname').val();
      if ( !unit_name_empty(jobunit, jobname) ) {
        return;
      } else if (jobunit!='') {
        getjobresult_byunit(jobunit).done(function(result) {
          console.log(result);

          $('section#jobresult_main').empty();
          printjobResults(result);
        });
      } else if (jobname!='') {
        getjobresult_byname(jobname).done(function(result) {
          console.log(result);

          $('section#jobresult_main').empty();
          printjobResults(result);
        });
      }
    });
  });
});


