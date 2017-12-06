
function getDataDrums() 
{
  alert("test");
  sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({

        url: "/getdrums",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
    drums = response;
          
          drums.forEach(function (drum) 
          {
             var nombre = "<div class='col-md-3 col-sm-3 wow fadeInUp' " +
        " data-wow-delay='0.2s'> " +
                        "<img src='" + drum.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + drum.marcadrum + "</h3>" +
                        "<h5>" + drum.modelodrum + "</h5>" +
                         "<h5>" + drum.tambores + "</h5>" +
                          "<h5>" + drum.precio + "</h5>" +
                        "</div>" +
                        "</div>" + 

                        
                       $("#drums").append(nombre);
                });
     
   }
        });          
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}

