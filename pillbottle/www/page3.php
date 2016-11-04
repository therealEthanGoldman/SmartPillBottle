<?PHP
session_start();
if (!(isset($_SESSION['login']) && $_SESSION['login'] != '')) {
	header ("Location: login3.php");
}

?>

	<html>
	<head>
	<title>IOT Device User Interface</title>


	</head>
	<body>




	<p><big><b>User Logged in</b></big></p>
	
	
	<p><b>Dosing Schedule</b></p>
	<table border cols=2>
	<tr><td>Time of dose</td><td>  amount </td></tr>
<?PHP  

$connection = mysql_connect('localhost', 'root', 'p3gasus'); 
mysql_select_db('iotdevdb',$connection);

$query = "SELECT * FROM doses"; 
$result = mysql_query($query);

while($row = mysql_fetch_array($result)){   //Creates a loop to loop through results
echo "<tr><td>" . $row[1] . "</td><td>" . $row[2] . "</td></tr>";  //$row['index'] the index here is a field name
}

echo "</table>"; //Close the table in HTML

mysql_close(); //Make sure to close out the database connection
?>
<p>  </p>

<FORM METHOD = "BEEP" ACTION="page3.php" >
<button type="button" onclick="parent.location='findme.php'">Find Me!</button>
</FORM>
	


<A HREF = page2.php>Log out</A>

	</body>
	</html>
