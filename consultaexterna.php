<?php
$apiToken = "919579060:AAFeo3wV8iwyDHhJhRvFlU2XzecfCftmn5U";
$chat_id= "227315570";
$connectDBexterno = mysqli_connect("sql10.freemysqlhosting.net", "sql10282729", "haM6SHtrmF", "sql10282729","3306");


     $texto = "Se ha realizado conección con base de datos";
     $texto2 = "No se pudo realizar conección con base de datos";

if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL EXTERNO: " . mysqli_connect_error();
     $urlfinal= "http://api.telegram.org/bot".$apiToken."/sendMessage?chat_id=".$chat_id. "&text=".$texto2;
     $urlfinal2 = preg_replace("/ /", "%20", $urlfinal);
     $response = file_get_contents($urlfinal2, false, stream_context_create($arrContextOptions));
  }else{
    echo "Conecto al servidor <br>";
         $urlfinal= "http://api.telegram.org/bot".$apiToken."/sendMessage?chat_id=".$chat_id. "&text=".$texto1;
     $urlfinal2 = preg_replace("/ /", "%20", $urlfinal);
     $response = file_get_contents($urlfinal2, false, stream_context_create($arrContextOptions));
  }
 

  
  ?>
