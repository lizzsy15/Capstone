<?php
  // Create connection
  $conn = mysqli_connect("db.soic.indiana.edu","i494f18_team34","my+sql=i494f18_team34","i494f18_team34");
  // Check connection
  if (!$conn) {
      die("Connection failed: " . mysqli_connect_error());
  }

  $avbeghj = mysqli_real_escape_string($conn, $_POST["avbeghj"]);
  $clubName = mysqli_real_escape_string($conn, $_POST["clubName"]);
  $description = mysqli_real_escape_string($conn, $_POST["description"]);
  print_r($clubName);
  print_r($description);
  if(isset($_FILES['image'])){
    $errors= array();
    $file_name = $_FILES['image']['name'];
    $file_size = $_FILES['image']['size'];
    $file_tmp = $_FILES['image']['tmp_name'];
    $file_type = $_FILES['image']['type'];
    $file_ext=strtolower(end(explode('.',$_FILES['image']['name'])));
    $expensions= array("jpeg","jpg","png");
    print_r($file_name);
    if($file_name!=""){
      if(in_array($file_ext,$expensions)=== false){
         $errors[]="extension not allowed, please choose a JPEG or PNG file.";
      }

      if($file_size > 2097152) {
         $errors[]='File size must be excately 2 MB';
      }

      if(str_word_count($clubName) == 0){
        $errors[]='No space in the club name';
      }

      if(file_exists("images/club/$file_name")){
        $num = 1;
        while(file_exists("images/club/$file_name")){
          $file_name = strtolower(current(explode('.',$file_name))).$num.'.'.$file_ext;
          $num += 1;
      }
	  }

      if(empty($errors)==true) {
         move_uploaded_file($file_tmp,"images/club/".$file_name);
         echo "Success";
         $sql = "INSERT INTO club (clubname, description, icon, userName)
         VALUES ('$clubName', '$description','$file_name','$avbeghj')";

         if (mysqli_query($conn, $sql)) {
           echo "New record created successfully";
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
  echo 'clubUploadContinue.cgi?clubName=';
  echo $clubName;
  echo "'";
  echo ')">';
  echo "<p>jsjsjsjs</p>
  </body>
  </html>";

         } else {
           echo "The club name is used!!";
		   echo "<a href='createClub.cgi'>Return</a>";
         }
         
      }
  }else{
	  $sql = "INSERT INTO club (clubname, description, userName)
         VALUES ('$clubName', '$description','$avbeghj')";

         if (mysqli_query($conn, $sql)) {
           echo "New record created successfully";
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
  echo 'clubUploadContinue.cgi?clubName=';
  echo $clubName;
  echo "'";
  echo ')">';
  echo "<p>jsjsjsjs</p>
  </body>
  </html>";

         } else {
           echo "The club name is used!!";
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
  echo 'clubUploadContinue.cgi?clubName=';
  echo $clubName;
  echo "'";
  echo ')">';
  echo "<a href='createClub.cgi'>Return</a>
  </body>
  </html>";

         }
		 mysqli_close($conn);
  }
  }
?>
