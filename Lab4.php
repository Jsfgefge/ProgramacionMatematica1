<?php 
	include("nc.php")
 ?>
<!DOCTYPE html>
<html>
<head>
	<title>Sontay</title>
</head>
<body>
<center>
	<fieldset>
		<legend>Sontay</legend>	
		<form action="Lab4.php" method="post">
			<input type="text" name="Codigo" placeholder="Ingrese codigo"><br>
			<input type="text" name="Nombre" placeholder="Ingrese nombre"><br>
			<input type="text" name="Sueldo" placeholder="Ingrese Sueldo"><br>
			<select name="Puesto">
				<option value="Gerente">Gerente</option>	
				<option value="Supervisor">Supervisor</option>
				<option value="Trabajador">Trabajador</option>
			</select><br>

			<input type="radio" name="r" value="#">Codigo: #<br>
			<input type="radio" name="r" value="@">Codigo: @<br>
			<input type="radio" name="r" value="$">Codigo: $<br>

			<input type="submit" name="btn" value="Insertar"><br>
			<input type="submit" name="btn" value="Mostrar"><br>

		</form>
	</fieldset>	
</center>
</body>
</html>
<?php 
if(isset($_POST['btn'])){
	$boton=$_POST['btn'];
	if($boton=="Insertar"){
		$Cod1=$_POST['Codigo'];
		$Nom=$_POST['Nombre'];
		$Suel=$_POST['Sueldo'];
		$Puesto=$_POST['Puesto'];
		$Cod2=$_POST['r'];
		$A1=0;
		$A2=0;
		if($Puesto=="Gerente"){
			$A1=$Suel*0.05;
		}
		if($Puesto=="Supervisor"){
			$A1=$Suel*0.04;
		}
		if($Puesto=="Trabajador"){
			$A1=$Suel*0.03;
		}

		if($Cod2=="#"){
			$A2=$Suel*0.045;
		}
		if($Cod2=="@"){
			$A2=$Suel*0.035;
		}
		if($Cod2=="$"){
			$A2=$Suel*0.025;
		}

		$tA=$A1+$A2;

		$tSuel=$Suel+$tA;

		$sql="insert into sueldos values('$Cod1','$Nom','$Suel','$Puesto','$Cod2','$A1','$A2','$tA','$tSuel')";
		mysql_query($sql);
		echo "Datos ingresados correctamente";
	}elseif ($boton=="Mostrar") {
		$sql="select *from sueldos";
		$w=mysql_query($sql);
		while($r=mysql_fetch_array($w)){
			echo"<table border='1'><tr><td>";
			echo"Codigo:".$r[0]."<br>";
			echo"Nombre:".$r[1]."<br>";
			echo"Sueldo:".$r[2]."<br>";
			echo"Puesto:".$r[3]."<br>";
			echo"_Codigo:".$r[4]."<br>";
			echo"aPuesto:".$r[5]."<br>";
			echo"aCodigo:".$r[6]."<br>";
			echo"tAumento:".$r[7]."<br>";
			echo"Nuevo Sueldo:".$r[8]."<br>";
			echo "</table></tr></td>";
		}
	}
}
 ?>
