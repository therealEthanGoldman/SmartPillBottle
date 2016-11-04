<?PHP
session_start();
if (!(isset($_SESSION['login']) && $_SESSION['login'] != '')) {
	header ("Location: login3.php");
}

?>
<?PHP


//==========================================
//	ESCAPE DANGEROUS SQL CHARACTERS
//==========================================
function quote_smart($value, $handle) {

   if (get_magic_quotes_gpc()) {
       $value = stripslashes($value);
   }

   if (!is_numeric($value)) {
       $value = "'" . mysql_real_escape_string($value, $handle) . "'";
   }
   return $value;
}

//==========================================
//	CONNECT TO THE LOCAL DATABASE
//==========================================
$db_user = "root";
$db_pass = "p3gasus";
$database = "iotdevdb";
$server = "127.0.0.1";

$db_handle = mysql_connect($server, $db_user, $db_pass);
$db_found = mysql_select_db($database, $db_handle);
if ($db_found) {
    $SQL = "SELECT * FROM settings ";
    $result = mysql_query($SQL);
    $num_rows = mysql_num_rows($result);

	//====================================================
	//	CHECK TO SEE IF THE $result VARIABLE IS TRUE
	//====================================================
	if ($num_rows) {
        $admin_email       = mysql_result($result, 0, 1);
	    $user_email        = mysql_result($result, 0, 2);
	    $user_name         = mysql_result($result, 0, 3);
	    $user_dose         = mysql_result($result, 0, 4);
	    $reorder_amount    = mysql_result($result, 0, 5);
	    $reminder_late     = mysql_result($result, 0, 6);
	    $cg_warning_late   = mysql_result($result, 0, 7);
	    $notes             = mysql_result($result, 0, 8);		   
	}
	else {
		$errorMessage = "No setting in DB";
	}

	mysql_close($db_handle);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST'){
	$admin_email = $_POST['admin_email'];
	$user_email = $_POST['user_email'];
	$user_name = $_POST['user_name'];
	$user_dose = $_POST['user_dose'];
	$reorder_amount = $_POST['reorder_amount'];
	$reminder_late = $_POST['reminder_late'];
	$cg_warning_late = $_POST['cg_warning_late'];
	$notes = $_POST['notes'];
	
	$admin_email = htmlspecialchars($admin_email);
	$user_email = htmlspecialchars($user_email);
	$user_name = htmlspecialchars($user_name);
	$user_dose = htmlspecialchars($user_dose);
	$reorder_amount = htmlspecialchars($reorder_amount);
	$reminder_late = htmlspecialchars($reminder_late);
	$cg_warning_late = htmlspecialchars($cg_warning_late);
	$notes = htmlspecialchars($notes); 
	//==========================================
	//	CONNECT TO THE LOCAL DATABASE
	//==========================================
	$dbo_handle = mysql_connect($server, $db_user, $db_pass);
	$dbo_found = mysql_select_db($database, $dbo_handle);
	if ($dbo_found) {
		$SQL = "UPDATE settings SET admin_email='$admin_email', user_email='$user_email', user_name='$user_name', user_dose='$user_dose', reorder_amount='$reorder_amount', reminder_late='$reminder_late', cg_warning_late='$cg_warning_late', notes='$notes'";
		$result = mysql_query($SQL);
	}
	else {
		$errorMessage = "No setting in DB";
	}

    mysql_close($dbo_handle);

}

?>

	<html>
	<head>
	<title>IOT Device Management Interface</title>


	</head>
	<body>




	<b><big>User Logged in </b> </big>


<P>
		<FORM NAME = 'form1' METHOD = "POST" ACTION ="page1.php">
		admin_email:     <input type="text" name="admin_email" value="<?php echo $admin_email;?>"> <P>
		user_email:      <input type="text" name="user_email" value="<?php echo $user_email;?>"> <P>
		user_name:       <input type="text" name="user_name" value="<?php echo $user_name;?>"> <P>
		user_dose:       <input type="text" name="user_dose" value="<?php echo $user_dose;?>"> <P>
		reorder_amount:  <input type="text" name="reorder_amount" value="<?php echo $reorder_amount;?>"> <P>
		reminder_late:   <input type="text" name="reminder_late" value="<?php echo $reminder_late;?>"> <P>
		cg_warning_late: <input type="text" name="cg_warning_late" value="<?php echo $cg_warning_late;?>"> <P>
		notes:           <input type="text" name="notes" value="<?php echo $notes;?>"> 
		<P>
		<INPUT TYPE = "Submit" NAME = "Submit" VALUE = "Save">
		</FORM>

<P></P>

<FORM METHOD = "BEEP" ACTION="page1.php" >
<button type="button" onclick="parent.location='findmea.php'">Find Me!</button>
</FORM>

<p></p>
		
<?PHP
$connection = mysql_connect('localhost', 'root', 'p3gasus'); 
mysql_select_db('iotdevdb',$connection);

$query = "SELECT * FROM iotlog"; //You don't need a ; like you do in SQL
$result = mysql_query($query);

echo "<table border cols=4>"; // start a table tag in the HTML

while($row = mysql_fetch_array($result)){   //Creates a loop to loop through results
echo "<tr><td>" . $row[0] . "</td><td>" . $row[1] . "</td><td>" . $row[2] . "</td><td>" . $row[3] . "</td></tr>";  //$row['index'] the index here is a field name
}

echo "</table>"; //Close the table in HTML

mysql_close(); //Make sure to close out the database connection
?>
<p/>
<A HREF = page2.php>Log out</A>

	</body>
	</html>
