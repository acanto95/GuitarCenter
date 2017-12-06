function getAllData(){
  getData();
  getDataDrums();
  getDataKeyboard();
  getDataBass();
}

function getData() 
{

	sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({
        url: "/gettweets",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
	  tweets = response;
          //alert(response);
          tweets.forEach(function (tweet) 
          {
             var nombre = "<div class='col-md-3' " +
        " '> " +
                        "<img src='" + tweet.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + tweet.marcagui + "</h3>" +
                        "<h5>" + tweet.modelogui + "</h5>" +
                         "<h5>" + tweet.cuerdas + "</h5>" +
                          "<h5>" + tweet.precio + "</h5>" +
                        "</div>" +
                        "</div>" 
                       $("#tweets").append(nombre);
                });
	   
 	 }
        });          
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}

function getDataDrums() 
{
 
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
             var nombre = "<div class='col-md-3' " +
        " '> " +
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
                        alert(drum.marcadrum);
                });

     
   }
        });  
              
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}


function getDataKeyboard() 
{
 
  sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({

        url: "/getkeyboards",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
    keyboards = response;
          
          keyboards.forEach(function (keyboard) 
          {
             var nombre = "<div class='col-md-3' " +
        " '> " +
                        "<img src='" + keyboard.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + keyboard.marcakey + "</h3>" +
                        "<h5>" + keyboard.modelokey + "</h5>" +
                         "<h5>" + keyboard.teclas + "</h5>" +
                          "<h5>" + keyboard.precio + "</h5>" +
                        "</div>" +
                        "</div>" + 

                        
                       $("#keyboards").append(nombre);

                });
     
   }
        });  
              
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}

function getDataBass() 
{
 
  sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({

        url: "/getbass",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
    basses = response;
          
          basses.forEach(function (bass) 
          {
             var nombre = "<div class='col-md-3' " +
        " '> " +
                        "<img src='" + bass.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + bass.marcabass + "</h3>" +
                        "<h5>" + bass.modelobass + "</h5>" +
                         "<h5>" + bass.cuerdas + "</h5>" +
                          "<h5>" + bass.precio + "</h5>" +
                        "</div>" +
                        "</div>" + 

                        
                       $("#basses").append(nombre);

                });
     
   }
        });  
              
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}



