<?php
  // Create connection
  $conn = mysqli_connect("db.soic.indiana.edu","i494f18_team34","my+sql=i494f18_team34","i494f18_team34");
  // Check connection
  if (!$conn) {
      die("Connection failed: " . mysqli_connect_error());
  }

  $boardName = mysqli_real_escape_string($conn, $_POST["boardName"]);
  $clubID = mysqli_real_escape_string($conn, $_POST["platform"]);

  $sql = "SELECT u.icon, u.username, cm.detail, cm.send_time FROM user as u, club_message as cm, club_user as cu
  WHERE cm.clubID = cu.clubID AND cm.userID = u.userID AND cm.clubID = $clubID
  GROUP BY club_messageID;";

  if (mysqli_query($conn, $sql)) {
    echo "New record created successfully";
  } else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
  }
  mysqli_close($conn);
?>
