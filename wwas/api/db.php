<?php

//dbx.php
class dbx
{
	public $connect;
	public $query;
	public $table;
	public $statement;

	function dbx()
	{	
		$this->connect =new PDO("mysql:host=localhost;dbname=YOUR_DB_NAME;", "YOUR_DB_USERNAME", "YOUR_DB_PASSWORD");
	}
	
	function makeConnection() {
		$this->connect =new PDO("mysql:host=localhost;dbname=YOUR_DB_NAME;", "YOUR_DB_USERNAME", "YOUR_DB_PASSWORD");	
	}
	
	function execute($data = null)
	{
		$this->statement = $this->connect->prepare($this->query);
		
		if($data)
		{
			$this->statement->execute($data);
		}
		else
		{
			$this->statement->execute();
		}		
	}

	function row_count()
	{
		return $this->statement->rowCount();
	}

	function statement_result()
	{
		return $this->statement->fetchAll();
	}

	function get_result()
	{
		return $this->connect->query($this->query, PDO::FETCH_ASSOC);
	}
	
	function exc_sel(){
		return $this->connect->query($this->query);
	}
	
	function getDataTable($tabe){
		return $tabe->fetchAll();
	}
	
	function get_row_count($qry){
		return $qry->fetchColumn();
	}
}
?>