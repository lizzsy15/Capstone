<?php
  // Create connection
  $conn = mysqli_connect("db.soic.indiana.edu","i494f18_team34","my+sql=i494f18_team34","i494f18_team34");
  // Check connection
  if (!$conn) {
      die("Connection failed: " . mysqli_connect_error());
  }

  $clubID = mysqli_real_escape_string($conn, $_GET["club"]);
  $clubName = mysqli_real_escape_string($conn, $_POST["clubName"]);
  $description = mysqli_real_escape_string($conn, $_POST["description"]);
  $status = true;

  if(isset($_FILES['image'])){
    $errors= array();
    $file_name = $_FILES['image']['name'];
    $file_size = $_FILES['image']['size'];
    $file_tmp = $_FILES['image']['tmp_name'];
    $file_type = $_FILES['image']['type'];
    $file_ext=strtolower(end(explode('.',$_FILES['image']['name'])));
    $expensions= array("jpeg","jpg","png");
    echo $file_name;
    if($file_name!=""){
      if(in_array($file_ext,$expensions)=== false){
         $errors[]="extension not allowed, please choose a JPEG or PNG file.";
      }

      if($file_size > 2097152) {
         $errors[]='File size must be excately 2 MB';
      }

      if(file_exists("images/club/$file_name")){
        // $errors[]="file alredy exists,please rename and upload again";
        $num = 1;
        while(file_exists("images/club/$file_name")){
          $file_name = strtolower(current(explode('.',$file_name))).$num.'.'.$file_ext;
          $num += 1;
        }
      }
      if(empty($errors)==true) {
         move_uploaded_file($file_tmp,"images/club/".$file_name);
         echo "Success";
      }
      else{
        echo $errors[0];
        echo "<html><head></head><body><p><a href='clubMessage.cgi?club=$clubID'>Return</a></p></body></html>";
        $status = false;
        if ($file_name==""){
          $status = true;
        }
      }

  }
  }

    echo '<html><head>
      <meta charset="utf-8">
      <title>Confirmation Page</title>
      <script>
      function goBack(name) {
        window.location.replace(name);
      }</script>
    </head>
    <body onload="';
    echo "goBack('";
    echo 'clubEditCont.cgi?clubID=';
    echo $clubID;
    echo "&clubName=";
	echo $clubName;
	echo "&description=";
	echo $description;
	echo "&file_name=";
	echo $file_name;
	echo "'";
    echo ')">';
    echo "
    </body>
    </html>";
?>
