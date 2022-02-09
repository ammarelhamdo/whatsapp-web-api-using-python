<?php
    
    include ('db.php');
        
    $status = false;
    $data = array();
    $acceptIP = 'YOUR SCRIPT IP INTERNET';
    $object = new dbx();
    $object->makeConnection();
    $link = $object->connect;
        
        
    if(!$link){        
        $error = "We can't connect with database, please call provide system";
    }
    else if (isset($_POST['action']) || isset($_GET['action'])) {
        if ($_POST['action'] == "createRequestMessage") {
            $object->query = "CALL createRequestMessage('1', '{$_POST['phone']}', '{$_POST['message']}', '{$_POST['type']}');";
            $object->execute();
            //$status = ($object->row_count() == 0);
            $status = true;
        }
        else if ($_GET['action'] == "requestsMessagesForUser" && $_SERVER['REMOTE_ADDR'] == $acceptIP) {
            $object->query = "CALL requestMessages('1');";   //1 is user id.
            $object->execute();
            
            $result = $object->statement_result();
            foreach($result as $row) {
                $dat = array();
                $dat['phone'] = $row['phone'];
                $dat['message'] = $row['message'];
                $dat['type'] = $row['type'];
                $data[] = $dat;
            }
            
            $status = true;
        } else {
            $status = false;
        }
    }
    
    $output = array(
        'status'    => $status,
        'data'      => $data
    );
    
    echo json_encode($output);
?>
