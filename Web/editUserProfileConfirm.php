<?php
  // Create connection
  $conn = mysqli_connect("db.soic.indiana.edu","i494f18_team34","my+sql=i494f18_team34","i494f18_team34");
  // Check connection
  if (!$conn) {
      die("Connection failed: " . mysqli_connect_error());
  }

  $userID = mysqli_real_escape_string($conn, $_GET["user"]);
  $nickname = mysqli_real_escape_string($conn, $_POST["nicknameEdit"]);
  $region = mysqli_real_escape_string($conn, $_POST["regionEdit"]);
  $gender = mysqli_real_escape_string($conn, $_POST["genderEdit"]);
  $dob = mysqli_real_escape_string($conn, $_POST["dobEdit"]);
  $description = mysqli_real_escape_string($conn, $_POST["descriptionEdit"]);
  $facebook = mysqli_real_escape_string($conn, $_POST["facebookEdit"]);
  $twitter = mysqli_real_escape_string($conn, $_POST["twitterEdit"]);
  $discord = mysqli_real_escape_string($conn, $_POST["DiscordEdit"]);
  $status = true;

  if(isset($_FILES['image'])){
    $errors= array();
    $file_name = $_FILES['image']['name'];
    $file_size = $_FILES['image']['size'];
    $file_tmp = $_FILES['image']['tmp_name'];
    $file_type = $_FILES['image']['type'];
    $file_ext=strtolower(end(explode('.',$_FILES['image']['name'])));
    $expensions= array("jpeg","jpg","png");
    if($file_name!=""){
      if(in_array($file_ext,$expensions)=== false){
         $errors[]="extension not allowed, please choose a JPEG or PNG file.";
      }

      if($file_size > 2097152) {
         $errors[]='File size must be excately 2 MB';
      }

      if(file_exists("images/user/$file_name")){
        // $errors[]="file alredy exists,please rename and upload again";
        $num = 1;
        while(file_exists("images/user/$file_name")){
          $file_name = strtolower(current(explode('.',$file_name))).$num.'.'.$file_ext;
          $num += 1;
        }
      }
      if(empty($errors)==true) {
         move_uploaded_file($file_tmp,"images/user/".$file_name);
         echo "Success";
         $sql = "update user set icon = '$file_name' where userID = $userID;";
         if (mysqli_query($conn, $sql)) {
           echo "New record created successfully";
         } else {
           echo "Error: " . $sql . "<br>" . mysqli_error($conn);
           echo "<html><head></head><body><a href='userProfile.cgi?userid=$userID'>Return</a></body></html>";
         }
      }
      else{
        echo $errors[0];
        echo "<html><head></head><body><p><a href='userProfile.cgi?userid=$userID'>Return</a></p></body></html>";
        $status = false;
        if ($file_name==""){
          $status = true;
        }
      }

    }
  }

  $sql = "update user set nickname = '$nickname', region = '$region',
  gender = '$gender', dob = '$dob', description = '$description',
  facebook = '$facebook', twitter = '$twitter', discord = '$discord' where userID = $userID;";

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
    if($status){
      echo "goBack('";
    }
    else{
      echo "goBack(";
    }
    echo 'userProfile.cgi?userid=';
    echo $userID;
    echo "'";
    echo ')">';
    echo "
    </body>
    </html>";
  } else {
    echo "No data is changed";
  }

?>
