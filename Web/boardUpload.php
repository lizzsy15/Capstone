<?php
  // Create connection
  $conn = mysqli_connect("db.soic.indiana.edu","i494f18_team34","my+sql=i494f18_team34","i494f18_team34");
  // Check connection
  if (!$conn) {
      die("Connection failed: " . mysqli_connect_error());
  }

  $avbeghj = mysqli_real_escape_string($conn, $_GET["avbeghj"]);
  $boardName = mysqli_real_escape_string($conn, $_POST["boardName"]);
  $platform = mysqli_real_escape_string($conn, $_POST["platform"]);
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

    if(str_word_count($boardName) == 0){
      $errors[]='No space in the board name';
    }

    if(file_exists("images/board/$platform/$file_name")){
      $num = 1;
      while(file_exists("images/board/$platform/$file_name")){
        $file_name = strtolower(current(explode('.',$file_name))).$num.'.'.$file_ext;
        $num += 1;
    }
	}

    if(empty($errors)==true) {
       move_uploaded_file($file_tmp,"images/board/$platform/$file_name");
       echo "Success";
       $sql = "INSERT INTO board (boardname, icon, platform, userID)
       VALUES ('$boardName', '$file_name', '$platform','$avbeghj')";

       if (mysqli_query($conn, $sql)) {
         echo "New record created successfully";
       } else {
         echo "Error: " . $sql . "<br>" . mysqli_error($conn);
       }
       mysqli_close($conn);
    }else{
       print_r($errors);
    }
}else{
	$sql = "INSERT INTO board (boardname, platform, userID)
       VALUES ('$boardName', '$platform','$avbeghj')";

       if (mysqli_query($conn, $sql)) {
         echo "New record created successfully";
       } else {
         echo "Error: " . $sql . "<br>" . mysqli_error($conn);
       }
       mysqli_close($conn);
}
  }
?>
<html>
<head><meta charset="utf-8">
<title>Confirmation Page</title>
<script>
function goBack(name) {
  window.location.replace(name);
}
</script></head>
    <!-- <body onload="goBack(boardMain.html')"> -->
    <body onload="goBack('boardMain.cgi')">
      <p>jsjsjsjs</p>
    </body>
    </html>
