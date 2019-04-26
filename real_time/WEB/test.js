const exec = require("child_process").exec;


let keyword = "python"
exec('gcloud dataproc jobs submit pyspark --cluster=cluster-56f5 --region=us-west1 data_processing.py -- ' + keyword, function(error, stdout, stderr){
    if(error){
      console.log(error)
    }
    console.info('cat child_process.js stdout: ');
    console.log(stdout);
});
